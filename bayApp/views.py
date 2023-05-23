from django.shortcuts import render
from django.contrib import messages
from .forms import *
import utils


def login(request):

    form = LoginForm()
    context = {
        "form": form
    }
    
    if request.method == "POST":
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            try:
                user = utils.authenticate_user(form.cleaned_data["email"], form.cleaned_data["password"])
                messages.success(request, f"Usuario autenticado correctamente con el UID {user.uid}")
            
            except Exception as e:
                
                messages.error(request, f"Error al autenticar usuario: {e}")
            
    
    return render(request, "login.html", context)

def signup(request):

    return render(request, "signup.html")

def landing(request):

    return render(request, "landing.html")

def details(request):

    return render(request, "details_prod.html")

