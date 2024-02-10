from django.shortcuts import render, get_object_or_404,redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product



def products_all(request):
    """ All products view, that includes sorting and queries """

    products = Product.objects.all()
    query = None
    

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'No search criteria has been entered yet!')
                redirect(reverse('products'))
    
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """ Single product details view """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

