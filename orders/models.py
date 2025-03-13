from django.db import models
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from cities_light.models import City

from foods.models import Pizza, Sandwich


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    country = CountryField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, blank=False)
    address = models.CharField(max_length=500)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=False, blank=False)
    order_note = models.CharField(max_length=500, blank=True)

    zarinpal_authority = models.CharField(max_length=100, blank=True)
    zarinpal_ref_id = models.CharField(max_length=100, blank=True)
    zarinpal_data = models.TextField(blank=True)

    datetime_created = models.DateTimeField('Created', auto_now_add=True, blank=False)
    datetime_modified = models.DateTimeField('Modified', auto_now=True)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    sandwich = models.ForeignKey(Sandwich, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()  # این فیلد حذف نشه

    def __str__(self):
        return f'OrderItem {self.id} or order {self.order.id}'

    def save(self, *args, **kwargs):
        if not self.price:  # اگر قیمت هنوز ذخیره نشده بود
            if self.pizza:
                self.price = self.pizza.price
            elif self.sandwich:
                self.price = self.sandwich.price
        super().save(*args, **kwargs)