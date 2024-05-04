from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag_view, name='bag_view'),
    path('add/<item_id>/', views.bag_add, name='bag_add'),
    path('remove/<item_id>/', views.bag_remove_item, name='bag_remove_item'),
]