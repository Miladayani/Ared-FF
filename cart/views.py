from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.apps import apps

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
    model = apps.get_model(app_label='foods', model_name=model_name)
    product = get_object_or_404(model, id=product_id)

    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])

    return redirect('sandwich_list')


def remove_from_cart_view(request, model_name, product_id):
    cart = Cart(request)

    # حذف محصول از سبد خرید
    cart.remove(f"{model_name}_{product_id}")

    return redirect('cart:cart_detail')