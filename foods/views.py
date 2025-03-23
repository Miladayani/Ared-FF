from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
        # context['pizza'] = get_object_or_404(Pizza, id=self.kwargs['pk'])
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
        # دریافت پارامتر مرتب‌سازی از URL
        order_by = self.request.GET.get('orderby', 'menu_order')

        # دریافت تمامی محصولات
        pizzas = Pizza.objects.all()
        sandwiches = Sandwich.objects.all()

        # اضافه کردن model_name به هر آیتم
        for pizza in pizzas:
            pizza.model_name = "Pizza"
        for sandwich in sandwiches:
            sandwich.model_name = "Sandwich"

        # ترکیب لیست‌ها
        products = list(pizzas) + list(sandwiches)

        # مرتب‌سازی بر اساس پارامتر دریافتی
        if order_by == 'date':
            products.sort(key=lambda x: x.date_created)
        elif order_by == 'newest':  # گزینه جدید
            products.sort(key=lambda x: x.date_created, reverse=True)
        elif order_by == 'price':
            products.sort(key=lambda x: x.price)
        elif order_by == 'price-desc':
            products.sort(key=lambda x: x.price, reverse=True)

        return products

    def get(self, request, *args, **kwargs):
        # اگر درخواست AJAX باشد، کل صفحه را بازگردانید
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            return render(request, self.template_name, context)
        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        parent_id = self.request.POST.get('parent_id')

        if parent_id and parent_id.strip():
            try:
                parent = Comment.objects.get(id=parent_id)
                obj.parent = parent

                # اطمینان از اینکه محصول از parent گرفته شود (برای تمام سطوح ریپلای)
                obj.pizza = parent.pizza if parent.pizza else None
                obj.sandwich = parent.sandwich if parent.sandwich else None

                print(f"Parent comment found: {obj.parent.id}")
            except Comment.DoesNotExist:
                print("ERROR: Parent comment not found!")
                obj.parent = None
        else:
            if 'pizza_id' in self.kwargs:
                obj.pizza = get_object_or_404(Pizza, id=self.kwargs['pizza_id'])
            elif 'sandwich_id' in self.kwargs:
                obj.sandwich = get_object_or_404(Sandwich, id=self.kwargs['sandwich_id'])

        obj.save()
        return redirect(self.get_success_url())

    # def post(self, request, *args, **kwargs):
    #     print("✅ درخواست POST به ویو رسید!")
    #
    #     form = self.get_form()
    #     if form.is_valid():
    #         print("✅ فرم معتبر است!")
    #         return self.form_valid(form)
    #     else:
    #         print("❌ فرم معتبر نیست! خطاها:", form.errors)
    #
    #     return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path

    def get_template_names(self):
        """بر اساس نوع محصول، قالب مناسب را انتخاب می‌کند"""
        if 'pizza_id' in self.kwargs:
            return ['foods/pizza_detail.html']
        elif 'sandwich_id' in self.kwargs:
            return ['foods/sandwich_detail.html']
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'pizza_id' in self.kwargs:
            pizza = get_object_or_404(Pizza, id=self.kwargs['pizza_id'])
            context['pizza'] = pizza
            # فقط کامنت‌های اصلی را نمایش می‌دهیم (بدون ریپلای‌ها)
            context['comments'] = pizza.comments.filter(active=True, parent=None)

        elif 'sandwich_id' in self.kwargs:
            sandwich = get_object_or_404(Sandwich, id=self.kwargs['sandwich_id'])
            context['sandwich'] = sandwich
            # فقط کامنت‌های اصلی را نمایش می‌دهیم (بدون ریپلای‌ها)
            context['comments'] = sandwich.comments.filter(active=True, parent=None)

        print(f"Comments loaded: {context['comments'].count()}")
        return context


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