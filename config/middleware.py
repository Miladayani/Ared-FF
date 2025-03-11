from django.shortcuts import redirect


class AdminAccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اگر کاربر به /admin/ یا /rosetta/ برود ولی staff یا superuser نباشد، او را ریدایرکت کن
        if (request.path.startswith('/admin/') or request.path.startswith('/rosetta/')) and not (
                request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
            return redirect('/no_access/')  # یا هر صفحه‌ای که برای عدم دسترسی تعیین کرده‌ای

        return self.get_response(request)