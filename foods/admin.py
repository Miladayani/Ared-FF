from django.contrib import admin

from .models import Pizza, Sandwich, Comment


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active', 'size', 'image', )


@admin.register(Sandwich)
class SandwichAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active', 'image', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_product', 'rating', 'author', 'body', 'email', 'date_created', 'active', 'profile_picture',  )
    list_filter = ('active', 'rating', 'date_created')
    search_fields = ('body', 'email', 'author__username', )

    def get_product(self, obj):
        return obj.pizza.title if obj.pizza else obj.sandwich.title
    get_product.short_description = 'Product'
