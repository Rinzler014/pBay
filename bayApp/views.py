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
    context = {"form": form}

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            try:
                user = firebase.auth().sign_in_with_email_and_password(
                    form.cleaned_data["email"], form.cleaned_data["password"]
                )
                messages.success(
                    request, f"Usuario {user['localId']} autenticado correctamente"
                )

                user = firebase.auth().sign_in_with_email_and_password(
                    form.cleaned_data["email"], form.cleaned_data["password"]
                )
                messages.success(
                    request, f"Usuario {user['localId']} autenticado correctamente"
                )

                return redirect("landing", user=user["localId"])

            except Exception as e:
                messages.error(request, "Usuario o Contraseña incorrectos")

    return render(request, "login.html", context)


def signup(request):
    form = CacheSignUpFormP1()
    context = {"form": form}

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
    context = {"form": form}

    if request.method == "POST":
        form = CacheSignUpFormP2(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES["personalID"]
            file_name = bson.ObjectId()
            file_extension = file.name.split(".")[-1]
            file_path = f"temp/{file_name}.{file_extension}"
            default_storage.save(file_path, file)

            form.cleaned_data["personalID"] = file_name
            form.cleaned_data["personalID_filename"] = (
                str(file_name) + "." + file_extension
            )

            request.session["location_info"] = json.dumps(
                form.cleaned_data, default=str
            )

            form.cleaned_data["personalID"] = str(file_name) + "." + file_extension

            request.session["location_info"] = json.dumps(
                form.cleaned_data, default=str
            )

            return redirect("signup_3")

        return render(request, "signup_2.html", context)

    return render(request, "signup_2.html", context)


def signup_3(request):
    form = SignUpForm(request=request)
    context = {"form": form}

    form = SignUpForm(request=request)
    context = {"form": form}


def signup_3(request):
    form = SignUpForm(request=request)
    context = {"form": form}

    if request.method == "POST":
        personal_info = json.loads(request.session["personal_info"])
        location_info = json.loads(request.session["location_info"])

        updated_data = request.POST.copy()
        updated_data.update(personal_info)
        updated_data.update(location_info)

        form = SignUpForm(updated_data, request=request)

        if form.is_valid():
            data = form.cleaned_data
            data["personalID_filename"] = location_info["personalID_filename"]
            data.pop("password2")

            try:
                user = auth.create_user_with_email_and_password(
                    data["email"], data["password"]
                )
                data.pop("password")
                db.child("users").child(user["localId"]).set(data)
                storage.child(f"users/{user['localId']}/personalID").put(
                    f"temp/{data['personalID']}"
                )
                print("Usuario creado correctamente")

                os.remove(f"temp/{data['personalID_filename']}")

                return redirect("login")

            except Exception as e:
                print(e)
                messages.error(request, f"Error al crear usuario: {e}")

    return render(request, "signup_3.html", context)


def landing(request, user):
    context = db.child("products").child("product1").get().val()

    context_list = [context] * 10

    return render(request, "landing.html", {"context_list": context_list, "user": user})


def edit_info_prod(request):
    form = EditInfoProductForm()
    context = {"form": form}

    if request.method == "POST":
        form = EditInfoProductForm(request.POST)

        if form.is_valid():
            try:
                print("Is valid")

                return redirect("login")

            except Exception as e:
                messages.error(request, f"Error al autenticar usuario: {e}")

    return render(request, "edit_info_prod.html", context)


def details(request):
    context = db.child("products").child("product1").get().val()

    return render(request, "details_prod.html", context)


def mis_ventas(request, user):
    prods = dict(db.child("products").get().val())
    num_vendidos = 0

    for product_id, product_data in prods.items():
        if product_data["availability"] == "Si":
            num_vendidos += 1

    nonum_vendidos = 0

    for product_id, product_data in prods.items():
        if product_data["availability"] == "No":
            nonum_vendidos += 1

    num_ventas = 0

    for product_id, product_data in prods.items():
        if product_data["num_ventas"] != 0:
            num_ventas += product_data["num_ventas"]

    tot_ventas = 0
    subtot = 0

    for product_id, product_data in prods.items():
        if product_data["price"] != 0 and product_data["num_ventas"] != 0:
            subtot += product_data["price"] * product_data["num_ventas"]
            tot_ventas += subtot

    prod_list = []
    for product_id, product_data in prods.items():
        if product_data["availability"] == "Si" and product_data["num_ventas"] != 0:
            prod_list.append(product_data)

    noprod_list = []
    for product_id, product_data in prods.items():
        if product_data["availability"] == "No" and product_data["num_ventas"] != 0:
            noprod_list.append(product_data)

    context = {
        "user": user,
        "num_vendidos": num_vendidos,
        "context_list": prod_list,
        "nocontext_list": noprod_list,
        "nonum_vendidos": nonum_vendidos,
        "num_ventas": num_ventas,
        "tot_ventas": tot_ventas,
    }

    return render(request, "mis_ventas.html", context)


def shopping_cart(request):
    return render(request, "shopping_cart.html")


def auctions(request, user_id):
    context = {
        "user": user_id,
        "bids": dict(db.child("auctions").get().val()),
    }

    return render(request, "bids.html", context)


def bids_state(request):
    return render(request, "bids_state.html")


def my_products(request):
    return render(request, "my_products.html")


def new_product(request):
    form = formNewProduct()
    context = {"form": form}

    return render(request, "new_product.html", context)


def bids_state(request, user_id):
    context = {
        "user": user_id,
        "auctions": dict(
            db.child("users").child(user_id).child("auctions").get().val()
        ),
    }

    return render(request, "bids_state.html", context)
