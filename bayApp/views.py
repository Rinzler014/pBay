from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import *
from utils import *
import json
import bson
from django.core.files.storage import FileSystemStorage, default_storage
import os


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
    
    if request.method == "POST":
        
        form = CacheSignUpFormP1(request.POST)
        print(form.is_valid())
        
        if form.is_valid():
            
            request.session["personal_info"] = json.dumps(form.cleaned_data)
            
            return redirect("signup_2")
        
        return render(request, "signup.html", context)

    return render(request, "signup.html", context)

def signup_2(request):

    form = CacheSignUpFormP2()
    context = {
        "form": form
    }

    if request.method == "POST":
        
        form = CacheSignUpFormP2(request.POST, request.FILES)
        
        if form.is_valid():
            
            file = request.FILES["personalID"]
            file_name = bson.ObjectId()
            file_extension = file.name.split(".")[-1]
            file_path = f"temp/{file_name}.{file_extension}"
            default_storage.save(file_path, file)
            
            form.cleaned_data["personalID"] = file_name
            form.cleaned_data["personalID_filename"] = str(file_name) + "." + file_extension

            request.session["location_info"] = json.dumps(form.cleaned_data, default=str)
            
            return redirect("signup_3")
            
        return render(request, "signup_2.html", context)
    
    return render(request, "signup_2.html", context)

def signup_3(request):

    form = SignUpForm()
    context = {
        "form": form
    }
    
    if request.method == "POST":
        
        personal_info = json.loads(request.session["personal_info"])
        location_info = json.loads(request.session["location_info"])
        
        updated_data = request.POST.copy()
        updated_data.update(personal_info)
        updated_data.update(location_info)
        
        form = SignUpForm(updated_data)
        
        if form.is_valid():
            
            data = form.cleaned_data
            data["personalID_filename"] = location_info["personalID_filename"]
            data.pop("password2")
            
            try:
                
                auth.create_user_with_email_and_password(data["email"], data["password"])
                data.pop("password")
                db.child("users").child(data["personalID"]).set(data)
                storage.child(f"users/{data['email']}/personalID").put(f"temp/{data['personalID_filename']}")
                print("Usuario creado correctamente")
                
                os.remove(f"temp/{data['personalID_filename']}")
                
                return redirect("login")
            
            except Exception as e:
                
                print(e)
    
    return render(request, "signup_3.html", context)

def landing(request):
    context = db.child("products").child("product1").get().val()

    context_list = [context] * 10

    return render(request, "landing.html", {"context_list": context_list})
    
def details(request):
    context = db.child("products").child("product1").get().val()

    return render(request, "details_prod.html", context)
