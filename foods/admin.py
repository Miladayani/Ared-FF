from django.contrib import admin

from .models import Pizza, Sandwich, Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = ('body', 'author', 'active', 'rating', )
    extra = 1


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'active', 'size', 'image', ]

    inlines = [
        CommentsInline,
    ]


@admin.register(Sandwich)
class SandwichAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'active', 'image', ]

    inlines = [
        CommentsInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_product', 'rating', 'author', 'body', 'email', 'date_created', 'active', ]
    list_filter = ['active', 'rating', 'date_created']
    search_fields = ['body', 'email', 'author__username', ]

    def get_product(self, obj):
        if obj.pizza:
            return obj.pizza.title
        elif obj.sandwich:
            return obj.sandwich.title
        return None
    get_product.short_description = 'Product'
