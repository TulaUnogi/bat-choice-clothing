from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from products.models import Product

def bag_view(request):
    """ A view to return the bag page """
    
    return render(request, "bag/bag.html")


def bag_add(request, item_id):
    """ Add product to the bag """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    request.session['bag'] = bag

    if item_id in list(bag.keys()):
        # capping the number of items at 1, as selling single items only
        bag[item_id] = 1
        messages.info(request, f'{ product.name } is already in your bag!')
    else:
        bag[item_id] = quantity
        messages.success(request, f'{ product.name } has been added to your bag!')

    return redirect(redirect_url)


def bag_remove_item(request, item_id):
    """ Remove product from the bag """

    try:

        bag = request.session.get('bag', {})

        bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:

        return HttpResponse(status=500)
