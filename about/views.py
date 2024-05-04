from django.shortcuts import (
    render,
    redirect,
    reverse)
from django.contrib import messages
from django.utils import timezone

from .forms import ReviewForm


def policies(request):
    """ A view to return the policies page """
    
    return render(request, "about/policies.html")


def faq(request):
    """ A view to return the faq page """
    
    return render(request, "about/faq.html")

def our_story(request):
    """ A view to return the faq page """
    
    return render(request, "about/our-story.html")

def reviews(request):
    """ A view to return the reviews page """
    form = ReviewForm()
    now = timezone.now()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = ReviewForm()
            form.order_review = form.cleaned_data['order_review']
            form.rating = form.cleaned_data['rating']
            form.order = form.cleaned_data['order']
            form.date = now
            if request.user.is_authenticated:
                form.customer = request.user.email
            else:
                form.customer = request.order.email
            form.save()
            messages.success(request, 'Thank you for sharing your opinion! \
                                        Your review has been submitted.')
            return redirect(reverse('reviews'))
        else:
            messages.error(request, "Sorry, there are some issues with your form. \
                Please ensure you enter a valid data.")

    template = "about/reviews.html"

    context = {
        'form': form,
    }

    return render(request, template, context)


