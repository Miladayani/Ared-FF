from django.urls import path

from . import views

urlpatterns = [
    path('', views.order_create_view, name='order_create'),
]