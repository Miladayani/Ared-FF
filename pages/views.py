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


class ServiceDetails(TemplateView):
    template_name = 'pages/servicedetails.html'


class Chef(TemplateView):
    template_name = 'pages/chef.html'


class ChefDetails(TemplateView):
    template_name = 'pages/chefdetails.html'


class Reservation(TemplateView):
    template_name = 'pages/reservation.html'


class Gallery(TemplateView):
    template_name = 'pages/gallery.html'


class ErrorPage(TemplateView):
    template_name = 'pages/error.html'