from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from cities_light.models import City
from .models import Order


class OrderForm(forms.ModelForm):
    country = CountryField().formfield(widget=CountrySelectWidget())  # ویجت انتخاب کشور
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),  # دریافت لیست شهرها
        widget=forms.Select(attrs={'class': 'form-control'})  # تنظیم ویجت
    )

    class Meta:
        model = Order
        fields = ['country', 'city', 'address', 'first_name', 'last_name', 'phone_number', 'order_note']