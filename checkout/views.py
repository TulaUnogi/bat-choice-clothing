from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse

from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm, DiscountForm
from .models import OrderLineItem, Order, Discount
from products.models import Product
from userprofile.forms import ProfileForm
from userprofile.models import UserProfile
from bag.contexts import in_bag
import stripe
import json


@require_POST
def cache_checkout_data(request):
    """A view to add info_save to payment intent"""
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(request.session.get("bag", {})),
                "info_save": request.POST.get("info_save"),
                "username": request.user,
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, we couldn't process your payment right now.\
                        Please try again later.",
        )
        return HttpResponse(content=e, status=400)


@require_POST
def add_discount(request):
    """Adds a discount to order"""
    form = DiscountForm(request.POST)
    if not form.is_valid():
        try:
            order_form = OrderForm()
            shop_discount = Discount.objects.filter(
                discount_code=request.POST.get("discount_code")
            ).first()
            request.session["discount_code"] = shop_discount.discount_code
            return render(
                request=request,
                template_name="checkout/checkout.html",
                context={"order_form": order_form},
            )
        except Discount.DoesNotExist:
            request.session["discount_id"] = None
            return redirect(reverse("checkout"))
            messages.error(
                request, "Invalid discount code! Please check if your code is correct!"
            )
    else:
        messages.error(
                request, "Invalid form! Please check if your data is correct!"
            )


def checkout(request):
    """A view to return the checkout page"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        bag = request.session.get("bag", {})
        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "address_line1": request.POST["address_line1"],
            "address_line2": request.POST["address_line2"],
            "region": request.POST["region"],
            "city": request.POST["city"],
            "postcode": request.POST["postcode"],
            "country": request.POST["country"],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            product_quantity=item_data,
                        )
                        order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One or more of the products in your bag \
                        hasn't been found in the database. Please contact us for assistance.",
                    )
                    order.delete()
                    return redirect(reverse("bag_view"))
                # except Product.quantity == 0:
                #     messages.error(request, "We're sorry, but one or more of the products \
                #         in your bag is already sold out!")
                #     order.delete()
                #     return redirect(reverse('bag_view'))
            request.session["info_save"] = "info_save" in request.POST
            return redirect(reverse("success_checkout_page", args=[order.order_number]))
        else:
            messages.error(
                request,
                "Oops! There was an error with your form! \
                Please make sure to provide correct information.",
            )

    else:
        bag = request.session.get("bag", {})
        if not bag:
            messages.error(request, "Oops! Nothing in your bag yet!")
            return redirect(reverse("products"))

        bag_now = in_bag(request)
        total = bag_now["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        order_form = OrderForm()

    # Prepopulates form with saved data if User is authenticated
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(
                initial={
                    "full_name": profile.saved_full_name,
                    "email": profile.user.email,
                    "phone_number": profile.saved_phone_number,
                    "country": profile.saved_country,
                    "postcode": profile.saved_postcode,
                    "city": profile.saved_city,
                    "address_line1": profile.saved_address_line1,
                    "address_line2": profile.saved_address_line2,
                    "region": profile.saved_region,
                }
            )
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            "Oops! Missing Stripe public key! \
            Please set it up in your environment!",
        )

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, template, context)


def success_checkout_page(request, order_number):
    """A view to handle successful checkout"""

    info_save = request.session.get("info_save")
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

    if info_save:
        profile_data = {
            "saved_full_name": order.full_name,
            "saved_email": order.email,
            "saved_phone_number": order.phone_number,
            "saved_address_line1": order.address_line1,
            "saved_address_line2": order.address_line2,
            "saved_city": order.city,
            "saved_region": order.region,
            "saved_postcode": order.postcode,
            "saved_country": order.country,
        }

        profile_form = ProfileForm(profile_data, instance=profile)
        if profile_form.is_valid():
            profile_form.save()

        messages.success(
            request,
            f"Your order number is {order_number}. \
        We will send you a confirmation email to {order.email}.",
        )

    if "bag" in request.session:
        del request.session["bag"]

    template = "checkout/success-checkout-page.html"
    context = {
        "order": order,
    }

    return render(request, template, context)
