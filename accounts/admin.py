from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # فقط نمایش فیلدهای username و email در لیست کاربران
    list_display = ('username', 'email')

    # حذف سایر فیلدها و نمایش فقط username و email در صفحه ویرایش کاربر
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
    )

    # تنظیم فیلدهای مورد نیاز در فرم افزودن کاربر
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

