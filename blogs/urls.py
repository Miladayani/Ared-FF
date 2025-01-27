from django.urls import path

from . import views

urlpatterns = [
    path('', views.Blog.as_view(), name='blog'),
    path('blog_detail', views.BlogDetail.as_view(), name='blog_detail'),
]