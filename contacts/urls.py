from django.urls import path

from . import views

urlpatterns = [
    path('', views.Contact.as_view(), name='contact'),
    path('send-email/', views.send_email, name='send_email'),
]