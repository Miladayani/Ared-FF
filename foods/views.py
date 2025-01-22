from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .forms import CommentForm
from .models import Pizza, Sandwich, Comment


class PizzaListView(ListView):
    queryset = Pizza.objects.filter(active=True, size='1')
    template_name = 'foods/pizza_list.html'
    context_object_name = 'pizzas'


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'foods/pizza_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizza'] = get_object_or_404(Pizza, id=self.kwargs['pk'])
        return context


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


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        pizza_id = int(self.kwargs['pizza_id'])
        pizza = get_object_or_404(Pizza, id=pizza_id)
        obj.pizza = pizza

        return super().form_valid(form)
