from django.urls import path
from .views import PizzaListView, SandwichListView, Shop, SandwichDetailView, PizzaDetailView, CommentCreateView, \
    filter_foods, search, get_product_details

urlpatterns = [
    path('pizzas/', PizzaListView.as_view(), name='pizza_list'),
    path('pizzas/<int:pk>/', PizzaDetailView.as_view(), name='pizza_detail'),
    path('sandwiches/', SandwichListView.as_view(), name='sandwich_list'),
    path('sandwiches/<int:pk>/', SandwichDetailView.as_view(), name='sandwich_detail'),
    path('shop', Shop.as_view(), name='shop'),
    path('filter-foods/', filter_foods, name='filter_foods'),
    path('search/', search, name='search'),
    path('product/<str:model_name>/<int:product_id>/', get_product_details, name='get_product_details'),
    path('pizza/<int:pizza_id>/comment/', CommentCreateView.as_view(), name='pizza_comment_create'),
    path('sandwich/<int:sandwich_id>/comment/', CommentCreateView.as_view(), name='sandwich_comment_create'),
]