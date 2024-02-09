from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.products_all, name='products'),
    path('<product_id>', views.product_details, name='product_details'),
]
 