from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<order_number>', views.success_checkout_page, name='success_checkout_page'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('add_discount/', views.add_discount, name='add_discount'),
    path('webhook/', webhook, name='webhook'),
]