from django.urls import path

from . import views

urlpatterns = [
    path('', views.RestaurantShop.as_view(), name='home'),
    path('aboutus', views.AboutUs.as_view(), name='aboutus'),
]
