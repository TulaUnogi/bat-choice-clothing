from django.shortcuts import render

def policies(request):
    """ A view to return the policies page """
    
    return render(request, "about/policies.html")
