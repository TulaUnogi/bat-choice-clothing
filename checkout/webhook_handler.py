from django.http import HttpResponse
from .models import Order, Product, OrderLineItem
from userprofile.models import UserProfile

import stripe
import json
import time


class Stripe_Webhook_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_webhook_event(self, event):
        """
        Handle various webhook events
        """
        return HttpResponse(
            content=f'Received a webhook: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle successful payment intent webhook
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        info_save = intent.metadata.info_save

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Cleaning shipping form data
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        # Update profile information after info_save is checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if info_save:
                profile.saved_full_name = shipping_details.name
                profile.saved_email = billing_details.email
                profile.saved_phone_number = shipping_details.phone
                profile.saved_country = shipping_details.address.country
                profile.saved_postcode = shipping_details.address.postal_code
                profile.saved_city = shipping_details.address.city
                profile.saved_address_line1 = (
                    shipping_details.address.line1
                    )
                profile.address_line2 = (
                    shipping_details.address.line2
                    )
                profile.saved_region = shipping_details.address.state
                profile.save()
        
        
        order_exists = False
        attempt = 1

        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    region__iexact=shipping_details.address.state,
                    city__iexact=shipping_details.address.city,
                    postcode__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        
        if order_exists:
            return HttpResponse(
                content=f'Received a webhook: {event["type"]} \
                | SUCCESS! This order is already in our database.',
                status=200
            )

        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    address_line1=shipping_details.address.line1,
                    address_line2=shipping_details.address.line2,
                    region=shipping_details.address.state,
                    city=shipping_details.address.city,
                    postcode=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            product_quantity=item_data,                            
                        )
                        order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Received a webhook: {event["type"]} \
                        | ERROR {e}',
                    status=500)
            return HttpResponse(
                content=f'Received a webhook: {event["type"]} \
                    | SUCCESS! Order in webhook has been created!',
                status=200
            )

    def handle_payment_intent_failed(self, event):
        """
        Handle unsuccessful payment intent webhook
        """
        return HttpResponse(
            content=f'Received a webhook: {event["type"]}',
            status=200
        )