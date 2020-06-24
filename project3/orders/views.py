from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
# Create your views here.

def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, "orders/login.html", {"message": None})
    context = {
        "categories": Category.objects.all()
    	}
    return render(request, "home.html", context)
