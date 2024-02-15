from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bag_view, name='bag_view'),
    path('add/<item_id>/', views.bag_add, name='bag_add'),
]