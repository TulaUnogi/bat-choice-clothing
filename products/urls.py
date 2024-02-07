from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.products_all, name='products'),
]
 