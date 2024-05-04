from django.shortcuts import render, get_object_or_404,redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm

from datetime import datetime, timedelta


def products_all(request):
    """ All products view, that includes sorting and queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    new_in = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'No search criteria has been entered yet!')
                redirect(reverse('products'))
    
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        if 'new_in' in request.GET:
            last_month = datetime.today() - timedelta(days=30)
            new_in = Product.objects.filter(added_on__gte=last_month)
            if not new_in:
                messages.info(request, 'No new products currently! \
                              Please come back at the next drop date!')


    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'count': products.count(),
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """ Single product details view """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only staff has permisssion to access this page.'
        )
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.info(request, 'Product added successfully!')
            return redirect(reverse('add_product'))
        else:
            messages.error(
                request, 'Failed to add product! Please ensure you entered correct data!'
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Update a product """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only staff has permisssion to access this page.'
        )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product! Please ensure you entered correct data!'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'Currently editing product: {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only staff has permisssion to access this page.'
        )
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect(reverse('products'))
