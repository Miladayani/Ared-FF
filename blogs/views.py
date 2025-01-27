from django.shortcuts import render
from django.views.generic import TemplateView


class Blog(TemplateView):
    template_name = 'blogs/blog.html'


class BlogDetail(TemplateView):
    template_name = 'blogs/blog_detail.html'
