from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
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

def menu(request , menu):
    try:
        menu = Category.objects.get(pk=menu)
    except:
        raise Http404("Pizza does not exist")
    context = {
        "menu": menu.category.all(),

        }
    return render(request, "orders/menu.html", context)
