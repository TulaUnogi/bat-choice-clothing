from django.shortcuts import render, get_object_or_404
from .models import Product



def products_all(request):
    """ All products view, that includes sorting and queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """ Single product details view """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

