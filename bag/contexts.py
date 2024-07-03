from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product


def in_bag(request):
    # Displays current bag contents and subtotal
    bag_items = []
    subtotal = 0

    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        product_count += quantity
        subtotal += quantity * product.price
        bag_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
            }
        )

    context = {
        "bag_items": bag_items,
        "subtotal": subtotal,
        "product_count": product_count,
    }

    return context
