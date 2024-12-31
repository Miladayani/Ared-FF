from django.db import models
from django.shortcuts import reverse


class Pizza(models.Model):
    PIZZA_SIZE = [
        ('1', 'Single one'),
        ('3', 'Family')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    size = models.CharField(max_length=10, choices=PIZZA_SIZE, default='1')
    # image =

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('food_detail', args=[self.pk])


class Sandwich(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    # image =

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('food_detail', args=[self.pk])