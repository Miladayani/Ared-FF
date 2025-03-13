import requests
import json

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.http import HttpResponse

from orders.models import Order


def payment_process(request):
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
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    res = requests.post(url=zarinpal_request_url, json=request_data, headers=request_header)
    data = res.json()

    print("Zarinpal Request Response:", data)  # لاگ برای بررسی

    if 'data' in data and isinstance(data['data'], dict) and 'authority' in data['data']:
        authority = data['data']['authority']
        order.zarinpal_authority = authority
        order.save()
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')

    elif 'errors' in data and isinstance(data['errors'], list) and len(data['errors']) > 0:
        error_message = data['errors'][0].get('message', 'خطای نامشخص')
        return HttpResponse(f"Error from Zarinpal: {error_message}")

    return HttpResponse("خطای نامشخص در ارتباط با زرین‌پال")


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': payment_authority,
        }

        res = requests.post(url='https://api.zarinpal.com/pg/v4/payment/verify.json', json=request_data, headers=request_header)
        data = res.json()

        print("Zarinpal Verify Response:", data)  # لاگ برای بررسی

        if 'data' in data and isinstance(data['data'], dict) and 'code' in data['data']:
            payment_code = data['data']['code']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['data'].get('ref_id', 'N/A')
                order.zarinpal_data = data
                order.save()
                return HttpResponse('پرداخت شما با موفقیت انجام شد.')

            elif payment_code == 101:
                return HttpResponse('پرداخت شما قبلاً تأیید شده است.')
            else:
                return HttpResponse(f"خطای پرداخت: {payment_code}")

    return HttpResponse('تراکنش ناموفق بود')


def payment_process_sandbox(request):
    # دریافت شناسه سفارش از سشن
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'merchant_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',  # تغییر به snake_case
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),  # اگر namespace اضافه کردی
    }

    res = requests.post(zarinpal_request_url, json=request_data, headers=request_header)
    data = res.json()

    if data.get('data') and 'authority' in data['data']:
        authority = data['data']['authority']
        order.zarinpal_authority = authority
        order.save()
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse(f"Zarinpal Request Failed: {data}")


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'merchant_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',  # تغییر به snake_case
            'amount': rial_total_price,
            'authority': payment_authority,
        }

        res = requests.post(
            url='https://sandbox.zarinpal.com/pg/v4/payment/verify.json',  # تغییر مسیر API
            json=request_data,  # ارسال json به جای data=json.dumps(...)
            headers=request_header,
        )

        data = res.json()

        if data.get('data') and 'code' in data['data']:
            payment_code = data['data']['code']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['data'].get('ref_id', 'N/A')
                order.zarinpal_data = data
                order.save()
                return HttpResponse('پرداخت شما با موفقیت انجام شد.')

            elif payment_code == 101:
                return HttpResponse('پرداخت شما با موفقیت انجام شد. البته این تراکنش قبلا ثبت شده است!')
            else:
                return HttpResponse(f"تراکنش ناموفق بود. کد خطا: {payment_code}")

    return HttpResponse('تراکنش ناموفق بود')