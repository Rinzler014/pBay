from django.shortcuts import render

# Create your views here.

def login(request):

    return render(request, "login.html")

def signup(request):

    return render(request, "signup.html")

def landing(request):

    return render(request, "landing.html")

def details(request):

    return render(request, "details_prod.html")

