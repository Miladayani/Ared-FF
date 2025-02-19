from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import reverse

from django.conf import settings
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizza_count'] = Pizza.objects.count()
        context['sandwich_count'] = Sandwich.objects.count()
        context['total_count'] = context['pizza_count'] + context['sandwich_count']
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        # بررسی وجود pizza_id یا sandwich_id در kwargs
        if 'pizza_id' in self.kwargs:
            obj.pizza = get_object_or_404(Pizza, id=self.kwargs['pizza_id'])
        elif 'sandwich_id' in self.kwargs:
            obj.sandwich = get_object_or_404(Sandwich, id=self.kwargs['sandwich_id'])

        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        # برگشت به صفحه جزئیات مدل صحیح
        if 'pizza_id' in self.kwargs:
            return reverse('pizza_detail', args=[self.kwargs['pizza_id']])
        elif 'sandwich_id' in self.kwargs:
            return reverse('sandwich_detail', args=[self.kwargs['sandwich_id']])


def filter_foods(request):
    food_type = request.GET.get('type', 'all')

    if food_type == 'pizzas':
        foods = list(Pizza.objects.values('id', 'title', 'price', 'image'))
        for food in foods:
            food['url'] = reverse('pizza_detail', args=[food['id']])  # لینک جزئیات پیتزا
            food['image'] = request.build_absolute_uri('/media/pizza/pizza_cover/' + food['image'].split('/')[-1])
    elif food_type == 'sandwiches':
        foods = list(Sandwich.objects.values('id', 'title', 'price', 'image'))
        for food in foods:
            food['url'] = reverse('sandwich_detail', args=[food['id']])  # لینک جزئیات ساندویچ
            food['image'] = request.build_absolute_uri('/media/sandwich/sandwich_cover/' + food['image'].split('/')[-1])
    else:
        pizzas = list(Pizza.objects.values('id', 'title', 'price', 'image'))
        for food in pizzas:
            food['url'] = reverse('pizza_detail', args=[food['id']])
            food['image'] = request.build_absolute_uri('/media/pizza/pizza_cover/' + food['image'].split('/')[-1])

        sandwiches = list(Sandwich.objects.values('id', 'title', 'price', 'image'))
        for food in sandwiches:
            food['url'] = reverse('sandwich_detail', args=[food['id']])
            food['image'] = request.build_absolute_uri('/media/sandwich/sandwich_cover/' + food['image'].split('/')[-1])

        foods = pizzas + sandwiches

    return JsonResponse(foods, safe=False)
