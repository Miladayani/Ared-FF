import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.http import JsonResponse, HttpResponseRedirect

from .cart import Cart
from .forms import AddToCartProductForm


def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['product_update_quantity_form'] = AddToCartProductForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })

    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def add_to_cart_view(request, product_id, model_name):
    cart = Cart(request)

    # دریافت مدل به‌صورت داینامیک
    try:
        model = apps.get_model(app_label='foods', model_name=model_name)
        product = get_object_or_404(model, id=product_id)
    except LookupError:
        # اگر مدل پیدا نشد، کاربر رو به صفحه‌ای دیگه هدایت کن
        return redirect('shop')

    # افزودن محصول به سبد خرید (به صورت پیش‌فرض ۱ عدد اضافه می‌شه)
    cart.add(product, quantity=1)

    # هدایت کاربر به صفحه‌ای مناسب (مثلاً صفحه سبد خرید یا صفحه محصولات)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # یا هر URL دیگه‌ای که مناسب باشه
# @require_POST
# def add_to_cart_view(request, product_id, model_name):
#     cart = Cart(request)
#
#     # دریافت مدل به‌صورت داینامیک
#     model = apps.get_model(app_label='foods', model_name=model_name)
#     product = get_object_or_404(model, id=product_id)
#
#     form = AddToCartProductForm(request.POST)
#
#     if form.is_valid():
#         cleaned_data = form.cleaned_data
#         quantity = cleaned_data['quantity']
#         cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])
#
#     return redirect('sandwich_list')


def remove_from_cart_view(request, model_name, product_id):
    cart = Cart(request)

    # حذف محصول از سبد خرید
    cart.remove(f"{model_name}_{product_id}")

    return redirect('cart:cart_detail')


@require_POST
@csrf_exempt
def update_cart_ajax(request, model_name, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", "{}")  # دریافت سبد خرید از سشن
        cart = json.loads(cart)  # تبدیل رشته JSON به دیکشنری

        product_key = f"{model_name}_{product_id}"  # کلید محصول در سبد خرید

        # دریافت داده‌های ارسالی از فرانت‌اند
        data = json.loads(request.body)
        action = data.get("action", None)
        price = data.get("price", 0)

        # بررسی وجود محصول در سبد خرید و مقدار پیش‌فرض
        if product_key not in cart:
            cart[product_key] = {
                "quantity": 0,
                "price": price,
                "product_id": product_id,
                "model_name": model_name
            }

        # افزایش یا کاهش تعداد محصول
        if action == "increase":
            cart[product_key]["quantity"] += 1
        elif action == "decrease":
            cart[product_key]["quantity"] = max(0, cart[product_key]["quantity"] - 1)
            if cart[product_key]["quantity"] == 0:
                del cart[product_key]  # اگر تعداد صفر شد، حذف از سبد

        request.session["cart"] = json.dumps(cart)  # ذخیره مجدد سبد در سشن

        # ارسال پاسخ به فرانت‌اند
        return JsonResponse({
            "success": True,
            "new_quantity": cart[product_key]["quantity"],
            "price": cart[product_key]["price"],
            "cart": cart,  # ارسال سبد خرید کامل
            "order_total": sum(int(item["price"]) * item["quantity"] for item in cart.values()),  # محاسبه دستی
        }, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)