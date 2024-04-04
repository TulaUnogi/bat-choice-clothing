from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
import stripe


def checkout(request):
    """ A view to return the checkout page """

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Oops! Nothing in your bag yet!')
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'stripe_public_key': 
                            'pk_test_51P1EyzRtag8MNdhxl3LG8hxyFeb3K2flCNNNRllvw1X12uG78gpAu0BVaQD6YgpOna3EK4TaK6BJnYyCwxXWDwRV00HWLSVWut',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)