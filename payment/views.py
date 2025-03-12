from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import requests
import json
from django.conf import settings

from orders.models import Order


def payment_process(request):
    # Get order id to pay
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': 'http://127.0.0.1:8000',
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()

    # بررسی می‌کنیم که آیا پاسخ یک دیکشنری است و کلید 'data' در آن وجود دارد یا خیر
    if isinstance(data, dict) and 'data' in data:
        authority_data = data['data']

        # بررسی می‌کنیم که آیا 'authority' در authority_data وجود دارد
        if 'authority' in authority_data:
            authority = authority_data['authority']
            order.zarinpal_authority = authority
            order.save()
        else:
            # هندل کردن خطای عدم وجود کلید 'authority'
            print("Authority key is missing in the response.")
    else:
        # هندل کردن خطای عدم وجود داده یا اشتباه بودن نوع پاسخ
        print("Response data is not a dictionary or missing 'data' key.")

    # data = res.json()['data']
    # authority = data['authority']
    # order.zarinpal_authority = authority
    # order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')