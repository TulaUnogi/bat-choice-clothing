from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Order
from products.models import Product
from bag.contexts import in_bag
import stripe


def checkout(request):
    """ A view to return the checkout page """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_line1': request.POST['address_line1'],
            'address_line2': request.POST['address_line2'],
            'address_line3': request.POST['address_line3'],
            'region': request.POST['region'],
            'city': request.POST['city'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
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
                    print('product does not exist')
                    messages.error(request, "One or more of the products in your bag \
                        hasn't been found in the database. Please contact us for assistance.")
                    order.delete()
                    return redirect(reverse('bag_view'))
                # except Product.quantity == 0:
                #     messages.error(request, "We're sorry, but one or more of the products \
                #         in your bag is already sold out!")
                #     order.delete()
                #     return redirect(reverse('bag_view'))
            print(f'Form valid {order}')
            request.session['info_save'] = 'info_save' in request.POST
            return redirect(reverse('success_checkout_page', args=[order.order_number]))
        else:
            messages.error(request, 'Oops! There was an error with your form! \
                Please make sure to provide correct information.')
            print('Form issues')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            print('No bag found!')
            messages.error(request, 'Oops! Nothing in your bag yet!')
            return redirect(reverse('products'))
        
        bag_now = in_bag(request)
        total = bag_now['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        print(f'{bag_now}')

    if not stripe_public_key:
        print('Oops! Missing Stripe public key! \
            Please set it up in your environment!')
        messages.warning(request, 'Oops! Missing Stripe public key! \
            Please set it up in your environment!')

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def success_checkout_page(request, order_number):
    """A view to handle successful checkout"""

    info_save = request.session.get('info_save')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Your order number is {order_number}. \
        We will send you a confirmation email to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/success-checkout-page.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
