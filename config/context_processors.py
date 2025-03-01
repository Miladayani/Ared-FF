from itertools import chain

from django.core.paginator import Paginator

from foods.models import Pizza, Sandwich


def global_products(request):
    pizzas = Pizza.objects.filter(active=True, size='1')
    sandwiches = Sandwich.objects.all()
    all_foods = list(chain(pizzas, sandwiches))  # ترکیب دو مدل

    # اعمال pagination
    paginator = Paginator(all_foods, 8)  # ۸ محصول در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {
        'page_obj': page_obj,  # صفحه‌بندی شده
        'total_count': len(all_foods)  # تعداد کل محصولات
    }


def food_counts(request):
    pizza_count = Pizza.objects.count()
    sandwich_count = Sandwich.objects.count()
    all_food_count = pizza_count + sandwich_count

    return {
        'pizza_count': pizza_count,
        'sandwich_count': sandwich_count,
        'all_food_count': all_food_count,
    }