from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import reverse
from itertools import chain
from django.core.paginator import Paginator

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
    paginate_by = 6
    template_name = 'foods/shop.html'
    context_object_name = 'shop'

    def get_queryset(self):
        pizzas = Pizza.objects.all()
        sandwiches = Sandwich.objects.all()

        # اضافه کردن model_name به هر آیتم
        for pizza in pizzas:
            pizza.model_name = "Pizza"
        for sandwich in sandwiches:
            sandwich.model_name = "Sandwich"

        return list(pizzas) + list(sandwiches)


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


def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # جستجو در مدل Pizza
        pizzas = Pizza.objects.filter(title__icontains=query).values('id', 'title')
        for pizza in pizzas:
            results.append({
                'type': 'Pizza',
                'id': pizza['id'],
                'title': pizza['title']
            })

        # جستجو در مدل Sandwich
        sandwiches = Sandwich.objects.filter(title__icontains=query).values('id', 'title')
        for sandwich in sandwiches:
            results.append({
                'type': 'Sandwich',
                'id': sandwich['id'],
                'title': sandwich['title']
            })

    return JsonResponse({'results': results})


def get_product_details(request, model_name, product_id):
    if model_name == 'Pizza':
        product = Pizza.objects.get(id=product_id)
    elif model_name == 'Sandwich':
        product = Sandwich.objects.get(id=product_id)
    else:
        return JsonResponse({'error': 'Invalid model name'}, status=400)

    data = {
        'title': product.title,
        'price': product.price,
        'description': product.description,
        'image_url': product.image.url,
    }
    return JsonResponse(data)