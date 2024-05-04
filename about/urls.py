from django.urls import path
from . import views

urlpatterns = [
    path('policies', views.policies, name='policies'),
    path('faq', views.faq, name='faq'),
    path('our-story', views.our_story, name='story'),
    path('reviews', views.reviews, name='reviews'),
]
 