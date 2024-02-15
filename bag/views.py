from django.shortcuts import render, redirect

def bag_view(request):
    """ A view to return the bag page """
    
    return render(request, "bag/bag.html")


def bag_add(request, item_id):
    """ Add product to the bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    request.session['bag'] = bag

    if item_id in list(bag.keys()):
        bag[item_id] = 1
    else:
        bag[item_id] = quantity

    return redirect(redirect_url)
