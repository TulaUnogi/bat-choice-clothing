from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('policies', views.policies, name='policies'),
    path('faq', views.faq, name='faq'),
    path('our-story', views.our_story, name='story'),
]
 