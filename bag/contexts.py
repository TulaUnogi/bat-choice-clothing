from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def in_bag(request):

    bag_items = []
    subtotal = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        product_count += quantity
        subtotal += quantity * product.price
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if subtotal < settings.FREE_SHIPPING_TRESHOLD:
        shipping = subtotal * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE / 100)
        free_shipping_delta = settings.FREE_SHIPPING_TRESHOLD - subtotal
        if shipping < settings.MINIMUM_SHIPPING_COST:
            shipping = settings.MINIMUM_SHIPPING_COST
    else:
        shipping = 0
        free_shipping_delta = 0
    
    grand_total = shipping + subtotal

    context = {
        'bag_items': bag_items,
        'subtotal': subtotal,
        'product_count': product_count,
        'shipping': shipping,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_treshold': settings.FREE_SHIPPING_TRESHOLD,
        'grand_total': grand_total,
    }

    return context
