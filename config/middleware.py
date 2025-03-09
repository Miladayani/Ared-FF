from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class AdminAccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # قبل از پردازش هر view می‌توانید بررسی‌های لازم را اینجا انجام دهید.

        # اگر کاربر به صفحه admin برود و admin نباشد، به صفحه no_access ریدایرکت شود.
        if request.path.startswith('/admin/') or request.path.startswith('/rosetta/') and not (
                request.user.is_staff or request.user.is_superuser):
            return redirect('/no_access/')

        # درخواست را به view بعدی ارسال کنید.
        response = self.get_response(request)

        return response