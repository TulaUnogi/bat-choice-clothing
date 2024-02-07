from django.shortcuts import render
from .models import Product



def products_all(request):
    """ All products view, that includes sorting and queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
