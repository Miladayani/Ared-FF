from django.apps import apps
import json
from django.contrib import messages


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.request = request

        self.session = request.session
        cart = self.session.get('cart', {})

        # تبدیل داده‌های ذخیره‌شده به دیکشنری (در صورت نیاز)
        if isinstance(cart, str):
            cart = json.loads(cart)

        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """ اضافه کردن محصول بدون ذخیره آبجکت مدل """
        model_name = product.__class__.__name__.lower()
        key = f"{model_name}_{product.id}"

        if key not in self.cart:
            self.cart[key] = {'quantity': 0, 'price': str(product.price), 'product_id': product.id,
                              'model_name': model_name}

        if replace_current_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity

        messages.success(self.request, 'Product successfully added to Cart.')

        self.save()

    def remove(self, product_id):
        """
        Remove a product from the cart.
        """
        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, 'Product successfully removed from Cart.')
            self.save()

    def save(self):
        """ ذخیره اطلاعات در سشن به‌صورت JSON-سریالایز‌شده """
        self.session['cart'] = json.dumps(self.cart)  # تبدیل دیکشنری به JSON
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        cart = self.cart.copy()
        product_map = {}

        for key in cart.keys():
            if "_" in key:
                model_name, product_id = key.split("_", 1)
                product_map.setdefault(model_name, []).append(product_id)

        products = {}
        for model_name, ids in product_map.items():
            try:
                Model = apps.get_model(app_label='foods', model_name=model_name)
                products.update({f"{model_name}_{p.id}": p for p in Model.objects.filter(id__in=ids)})
            except LookupError:
                continue

        for key, item in cart.items():
            item['product_obj'] = products.get(key, None)  # مقداردهی درون حلقه، نه ذخیره در سبد خرید
            item['total_price'] = item['product_obj'].price * item['quantity'] if item['product_obj'] else 0
            yield item

    def __len__(self):
        """
        تعداد کل آیتم‌های سبد خرید.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        پاک کردن تمامی محتویات سبد خرید.
        """
        del self.session['cart']
        self.save()

    def get_total_price(self):
        """
        محاسبه کل مبلغ سبد خرید.
        """
        return sum(
            int(item['product_obj'].price) * item['quantity']
            for item in self.cart.values() if item['product_obj']
        )