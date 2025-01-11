from itertools import chain
from foods.models import Pizza, Sandwich


def global_products(request):
    pizzas = Pizza.objects.filter(active=True, size='1')
    sandwiches = Sandwich.objects.all()
    all_foods = list(chain(pizzas, sandwiches))

    return {'pizzas': pizzas, 'sandwiches': sandwiches, 'all_foods': all_foods}