from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import UserProfile
from checkout.models import Order
from .forms import ProfileForm


@login_required
def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Successfully updated your profile!')
        else:
            messages.error(
                request, 'Failed to update profile! \
                          Please ensure you entered correct data!'
            )

    form = ProfileForm(instance=profile)
    orders = profile.orders.all()


    template = 'userprofile/user-profile.html'
    context = {
        'form': form,
        'orders': orders,
    }

    return render(request, template, context)


@login_required
def delete_profile(request):

    user = get_object_or_404(User, id=request.user.id)

    try:
        user.delete()
        messages.success(request, 'Your profile has been deleted successfully!')
        return redirect('home')
    except Exception as e: 
        messages.error(request, f'Oops! Error occured: {e}')
        return redirect('home')


@login_required
def order_history(request, order_number):
    """Get user's order history """

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'Displaying past order {order_number}.'
        'A confirmation email was sent on the date the order was made.'
    ))

    template = 'checkout/success-checkout-page.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
