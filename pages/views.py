from django.views.generic import TemplateView


class RestaurantShop(TemplateView):
    template_name = 'home.html'


class HomeFastFood(TemplateView):
    template_name = 'home2.html'


class HomeRestaurant(TemplateView):
    template_name = 'home3.html'


class AboutUs(TemplateView):
    template_name = 'pages/aboutus.html'


class Service(TemplateView):
    template_name = 'pages/service.html'


class ServiceDetail(TemplateView):
    template_name = 'pages/service_detail.html'


class ErrorPage(TemplateView):
    template_name = 'pages/error.html'


class Chef(TemplateView):
    template_name = 'pages/chef.html'


class ChefsDetail(TemplateView):
    template_name = 'pages/chefs_detail.html'


class Gallery(TemplateView):
    template_name = 'pages/gallery.html'


class WishList(TemplateView):
    template_name = 'pages/wishlist.html'

