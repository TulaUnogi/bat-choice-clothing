from django.shortcuts import render

def policies(request):
    """ A view to return the policies page """
    
    return render(request, "about/policies.html")


def faq(request):
    """ A view to return the faq page """
    
    return render(request, "about/faq.html")

def our_story(request):
    """ A view to return the faq page """
    
    return render(request, "about/our-story.html")
