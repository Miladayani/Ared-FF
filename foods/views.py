from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Pizza, Sandwich


class PizzaListView(ListView):
    queryset = Pizza.objects.filter(active=True)
    template_name = 'foods/foods_list.html'
    context_object_name = 'pizzas'


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'foods/food_detail.html'
    context_object_name = 'pizza'


class SandwichListView(ListView):
    queryset = Sandwich.objects.filter(active=True)
    template_name = 'foods/foods_list.html'
    context_object_name = 'sandwiches'


class SandwichDetailView(DetailView):
    model = Sandwich
    template_name = 'foods/food_detail.html'
    context_object_name = 'sandwich'
