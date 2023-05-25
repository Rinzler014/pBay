from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import *
from utils import *


def login(request):

    form = LoginForm()
    context = {
        "form": form
    }
    
    if request.method == "POST":
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            try:
                user = firebase.auth().sign_in_with_email_and_password(form.cleaned_data["email"], form.cleaned_data["password"])
                messages.success(request, f"Usuario {user['localId']} autenticado correctamente") 
            
            except Exception as e:
                
                messages.error(request, f"Error al autenticar usuario: {e}")
            
    
    return render(request, "login.html", context)

def signup(request):
    
    form = CacheSignUpFormP1()
    context = {
        "form": form
    }

    return render(request, "signup.html", context)

def landing(request):

    return render(request, "landing.html")

def details(request):
    context = db.child("products").child("product1").get().val()

    return render(request, "details_prod.html", context)

def signup_2(request):

    return render(request, "signup_2.html")

