from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'first_name', 'last_name', 'phone_number', 'order_note']