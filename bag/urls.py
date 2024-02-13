from django.urls import path, include
from . import views

urlpatterns = [
    path('bag', views.bag, name='bag'),
]