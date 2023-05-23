from django.shortcuts import render
from .forms import *
import utils


def login(request):

    form = LoginForm()
    context = {
        "form": form
    }
    
    return render(request, "login.html", context)

def signup(request):

    return render(request, "signup.html")

def landing(request):

    return render(request, "landing.html")

def details(request):

    return render(request, "details_prod.html")

