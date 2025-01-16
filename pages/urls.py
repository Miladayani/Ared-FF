from django.urls import path

from . import views

urlpatterns = [
    path('', views.RestaurantShop.as_view(), name='home'),
    path('home2', views.HomeFastFood.as_view(), name='home2'),
    path('home3', views.HomeRestaurant.as_view(), name='home3'),
    path('aboutus', views.AboutUs.as_view(), name='aboutus'),
]
