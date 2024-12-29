from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Food


class FoodListView(ListView):
    queryset = Food.objects.filter(active=True)
    template_name = 'foods/foods_list.html'
    context_object_name = 'foods'


class FoodDetailView(DetailView):
    model = Food
    template_name = 'foods/food_detail.html'
    context_object_name = 'food'
