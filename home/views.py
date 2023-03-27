from django.shortcuts import render
from django.views.generic import TemplateView, DetailView


# Create your views here.

class Homepage(TemplateView):
    template_name = 'homepagetest.html'


class Webshop(TemplateView):
    template_name = 'webshop.html'
