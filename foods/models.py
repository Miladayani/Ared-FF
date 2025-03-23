from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Pizza(models.Model):
    PIZZA_SIZE = [
        ('1', 'Single one'),
        ('3', 'Family')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    size = models.CharField(max_length=10, choices=PIZZA_SIZE, default='1')
    image = models.ImageField(upload_to='pizza/pizza_cover', blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pizza_detail', args=[self.pk])


class Sandwich(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='sandwich/sandwich_cover', blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sandwich_detail', args=[self.pk])


class Comment(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    sandwich = models.ForeignKey(Sandwich, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)], blank=True, null=True)  # امتیاز از 1 تا 5
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    email = models.EmailField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        if self.pizza:
            return reverse('pizza_detail', args=[self.pizza.id])
        elif self.sandwich:
            return reverse('sandwich_detail', args=[self.sandwich.id])
