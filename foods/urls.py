from django.urls import path
from .views import PizzaListView, SandwichListView, Shop

urlpatterns = [
    path('pizzas/', PizzaListView.as_view(), name='pizza_list'),
    # path('pizzas/<int:pk>/', PizzaDetailView.as_view(), name='pizza_detail'),
    path('sandwiches/', SandwichListView.as_view(), name='sandwich_list'),
    # path('sandwiches/<int:pk>/', SandwichDetailView.as_view(), name='sandwich_detail'),
    path('shop', Shop.as_view(), name='shop'),
]