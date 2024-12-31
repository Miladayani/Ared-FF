from django.contrib import admin

from .models import Pizza, Sandwich


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active', 'size')


@admin.register(Sandwich)
class SandwichAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active',)