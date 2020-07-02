from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {"message": None})
    model = Category
    template_name = 'home.html'
    context = {
        "categories": Category.objects.all()
        }
    return render(request, "orders/home.html", context)

def menu(request , pizza_type):
    try:
        pizza = pizza_type.objects.all()
    except pizza_type.DoesNotExist:
        raise Http404("Pizza does not exist")
    context = {
        "pizzas": pizza
        }
    return render(request, "orders/menu.html", context)
