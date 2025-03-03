# Generated by Django 5.1.4 on 2025-02-08 09:19

import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('foods', '0006_remove_comment_profile_picture_alter_comment_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('address', models.CharField(max_length=500)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('order_note', models.CharField(blank=True, max_length=500)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foods.pizza')),
                ('sandwich', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foods.sandwich')),
            ],
        ),
    ]
