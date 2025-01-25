from django.urls import path

from . import views

urlpatterns = [
    path('', views.RestaurantShop.as_view(), name='home'),
    path('home2', views.HomeFastFood.as_view(), name='home2'),
    path('home3', views.HomeRestaurant.as_view(), name='home3'),
    path('aboutus', views.AboutUs.as_view(), name='aboutus'),
    path('error', views.ErrorPage.as_view(), name='error'),
    path('service', views.Service.as_view(), name='service'),
    path('service_detail', views.ServiceDetail.as_view(), name='service_detail'),
    path('chef', views.Chef.as_view(), name='chef'),
    path('chefs_detail', views.ChefsDetail.as_view(), name='chefs_detail'),
    path('gallery', views.Gallery.as_view(), name='gallery'),
]
