from django.urls import path
from . import views


urlpatterns = [
    path('', views.products_all, name='products'),
    path('<int:product_id>/', views.product_details, name='product_details'),
    path('add/', views.add_product, name='add_product'),
    path('<int:product_id>/edit', views.edit_product, name='edit_product'),
    path('<int:product_id>/delete', views.delete_product, name='delete_product'),
]
 