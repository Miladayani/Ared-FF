from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.cart import Cart
from foods.models import Pizza, Sandwich
from .forms import OrderForm
from .models import OrderItem


@login_required()
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'You can not proceed to checkout page because your cart is empty.')
        return redirect('shop')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product_id = item.get('product_id')
                product_type = item.get('model_name')

                if not product_id or not product_type:
                    continue  # رد کردن موارد نامعتبر

                if product_type == 'pizza':
                    OrderItem.objects.create(
                        order=order_obj,
                        pizza_id=product_id,  # ذخیره فقط ID
                        quantity=item['quantity'],
                    )
                elif product_type == 'sandwich':
                    OrderItem.objects.create(
                        order=order_obj,
                        sandwich_id=product_id,  # ذخیره فقط ID
                        quantity=item['quantity'],
                    )

            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id
            return redirect('payment:payment_process')

    return render(request, 'orders/order_create.html', {
        'form': order_form,
    })
