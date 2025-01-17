from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Pizza, Sandwich


class PizzaListView(ListView):
    queryset = Pizza.objects.filter(active=True, size='1')
    template_name = 'foods/pizza_list.html'
    context_object_name = 'pizzas'


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'foods/pizza_detail.html'
    context_object_name = 'pizza'


class SandwichListView(ListView):
    queryset = Sandwich.objects.filter(active=True)
    template_name = 'foods/sandwich_list.html'
    context_object_name = 'sandwiches'


class SandwichDetailView(DetailView):
    model = Sandwich
    template_name = 'foods/sandwich_detail.html'
    context_object_name = 'sandwich'


class Shop(ListView):
    template_name = 'foods/shop.html'
    context_object_name = 'shop'

    def get_queryset(self):
        return list(Pizza.objects.all()) + list(Sandwich.objects.all())
