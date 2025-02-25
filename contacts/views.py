from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class Contact(TemplateView):
    template_name = 'contacts/contact.html'


@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # متن ایمیل به‌صورت HTML
        html_message = f"""
        <h3>مشخصات کاربر:</h3>
        <table border="1" cellpadding="10" cellspacing="0">
            <tr>
                <th>نام</th>
                <td>{name}</td>
            </tr>
            <tr>
                <th>ایمیل</th>
                <td>{email}</td>
            </tr>
            <tr>
                <th>شماره تلفن</th>
                <td>{phone}</td>
            </tr>
            <tr>
                <th>موضوع</th>
                <td>{subject}</td>
            </tr>
        </table>
        <h3>پیام:</h3>
        <p>{message}</p>
        """

        try:
            # ارسال ایمیل با محتوای HTML
            send_mail(
                subject,  # موضوع ایمیل
                'This is a plain text version of the email.',  # نسخه متنی ایمیل (اختیاری)
                email,  # ایمیل فرستنده (از کاربر)
                ['your-email@gmail.com'],  # ایمیل دریافت‌کننده (شما)
                html_message=html_message,  # محتوای HTML
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'ایمیل با موفقیت ارسال شد!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})