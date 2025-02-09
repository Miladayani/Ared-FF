from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'pizza', 'sandwich', 'quantity', ]
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'datetime_created', 'is_paid', 'country', 'city', ]

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'pizza', 'sandwich', 'quantity', ]