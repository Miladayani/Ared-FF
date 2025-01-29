from foods.models import Pizza, Sandwich


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add the specified pizza or sandwich to the cart if it exists.
        """
        if not isinstance(product, (Pizza, Sandwich)):
            return  # اگر محصول از نوع Pizza یا Sandwich نباشد، متوقف شود

        product_id = f"{product.__class__.__name__.lower()}_{product.id}"

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        """
        Remove a pizza or sandwich from the cart
        """
        if not isinstance(product, (Pizza, Sandwich)):
            return

        product_id = f"{product.__class__.__name__.lower()}_{product.id}"

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        cart = self.cart.copy()

        pizzas = Pizza.objects.filter(id__in=[pid.split('_')[1] for pid in product_ids if pid.startswith('pizza')])
        sandwiches = Sandwich.objects.filter(
            id__in=[pid.split('_')[1] for pid in product_ids if pid.startswith('sandwich')])

        for product in pizzas:
            cart[f"pizza_{product.id}"]['product_obj'] = product

        for product in sandwiches:
            cart[f"sandwich_{product.id}"]['product_obj'] = product

        for item in cart.values():
            yield item

    def __len__(self):
        return len(self.cart.keys())

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()
        pizzas = Pizza.objects.filter(id__in=product_ids)
        sandwiches = Sandwich.objects.filter(id__in=product_ids)

        return sum(item.price for item in pizzas) + sum(item.price for item in sandwiches)