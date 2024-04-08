from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<order_number>', views.success_checkout_page, name='success_checkout_page'),
]