from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail_view, name='cart_detail'),
    path('add/<str:model_name>/<int:product_id>/', views.add_to_cart_view, name='cart_add'),
    path('remove/<str:model_name>/<int:product_id>/', views.remove_from_cart_view, name='cart_remove'),
    path('update/<str:model_name>/<int:product_id>/', views.update_cart_ajax, name='update_cart_ajax'),
]