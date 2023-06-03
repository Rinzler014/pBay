from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import *
from utils import *
import json
import bson
from django.core.files.storage import FileSystemStorage, default_storage
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('./serAccountKey.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def login(request):
    form = LoginForm()
    context = {"form": form}

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            
            try:
                user = auth.sign_in_with_email_and_password(
                    form.cleaned_data["email"], form.cleaned_data["password"]
                )
                messages.success(
                    request, f"Usuario {user['localId']} autenticado correctamente"
                )

                return redirect("landing", user_id=user["localId"])

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

            form.cleaned_data["personalID_file"] = str(file_name) + "." + file_extension

            request.session["location_info"] = json.dumps(
                form.cleaned_data, default=str
            )

            return redirect("signup_3")

        return render(request, "signup_2.html", context)

    return render(request, "signup_2.html", context)


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
            data["personalID_file"] = location_info["personalID_file"]
            data.pop("password2")

            try:
                user = auth.create_user_with_email_and_password(
                    data["email"], data["password"]
                )
                data.pop("password")
                data["type"] = "user"
                db.collection("users").document(user["localId"]).set(data)
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


def landing(request, user_id):
    
    platform_products = db.collection("products").stream()
    
    products = [{product.id : product.to_dict()} for product in platform_products]
    
    context = {
        "user": user_id,
        "products": products,
    }

    return render(request, "landing.html", context)


def edit_info_prod(request, user_id):
    form = formEditInfoProduct()

    productID = "pruebaOmar"

    context = {
        "user": user_id,
        "form": form,
    }

    if request.method == "POST":
        
        form = formEditInfoProduct(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            file = request.FILES["images"]
            file_name = bson.ObjectId()
            file_extension = file.name.split(".")[-1]
            file_path = f"temp/{file_name}.{file_extension}"
            default_storage.save(file_path, file)
            
            storage.child(f"products/{productID}/{file_name}").put(file_path)

            urlImages = []

            for image in request.FILES.getlist('images'):
                    
                    nombre_imagen = image.name
                    
                    file_extension = nombre_imagen.split(".")[-1]
                    file_path = f"temp/{nombre_imagen}.{file_extension}"
                    
                    default_storage.save(file_path, image)
                    
                    ruta_guardado = f"products/{productID}/{nombre_imagen}"
                    storage.child(ruta_guardado).put(file_path)

                    storage_path = storage.child(ruta_guardado).get_url("2")
        
                    urlImages.append(storage_path)
                    os.remove(file_path)
            
            optionSale = form.cleaned_data['option']
            
            if optionSale == 'subasta':
                dataP = {
                    u"title": data['title'],
                    u"description": data['description'],
                    u"urlImages": urlImages,
                    u"price": data['price'],
                    u"stock": data['stock'],
                    u"optionSale": data['option'],
                    u"startingPrice": data['startingPrice'],
                    u"durationDays": data['durationDays'],
                    u"priceCI": data['priceCI']
                    }
                db.collection('products').document(productID).set(dataP)

            else:
                dataP = {
                    u"title": data['title'],
                    u"description": data['description'],
                    u"urlImages": urlImages,
                    u"price": data['price'],
                    u"stock": data['stock'],
                    u"optionSale": data['option'],
                    }
                db.collection('products').document(productID).set(dataP)
            

    return render(request, "edit_info_prod.html", context)


def details(request):
    prodDetails = db.collection("products").document("5zSNGRaS8BFVOgpkDHhw").get().to_dict()
    context =  prodDetails
    # prodDetails["prodDetailsEstado"],
    # prodDetails["Images"],
    # prodDetails["category"],
    # prodDetails["condition"],
    # prodDetails["featured"],
    # prodDetails["isAuction"],
    # prodDetails["manufacturer"],
    # prodDetails["model"],
    # prodDetails["price"],
    # prodDetails["productDescription"],
    # prodDetails["productName"],
    # prodDetails["publicationTime"],
    # prodDetails["quantity"],
    # prodDetails["sellerID"],
    # prodDetails["subcategory"],
    # prodDetails["totalSales"],
    # prodDetails["visits"],

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


def shopping_cart(request, user_id):
    
    context = {
        "user": user_id,
    }
    
    return render(request, "shopping_cart.html", context)


def auctions(request, user_id):
    
    platform_bids = db.collection("subasta").stream()
    
    bids = [{bid.id : bid.to_dict()} for bid in platform_bids]
    
    context = {
        "user": user_id,
        "bids": bids,
    }

    return render(request, "bids.html", context)


def bids_state(request, user_id):
    
    user_bids = db.collection(u"users").document(user_id).collection("bids").stream()

    
    bids = [{bid.id : bid.to_dict()} for bid in user_bids]
    
    
    context = {
        "user": user_id,
        "bids": bids,
    }

    return render(request, "bids_state.html", context)


def my_products(request, user_id):

    print(user_id)
    print(user_id)
    print(user_id)
    platform_products = db.collection("products").where("sellerID", "==", user_id).stream()
    products = [{product.id: product.to_dict()} for product in platform_products]

    print(products)

    context = {
        "user": user_id,
        "products": products,
    }
    return render(request, "my_products.html", context)



def new_product(request, user_id):
    form = formNewProduct()

    productName = str(bson.ObjectId())


    context = {
        "user": user_id,
        "form": form,
    }

    if request.method == "POST":
        
        form = formNewProduct(request.POST, request.FILES)
        
        if form.is_valid():
            
            data = form.cleaned_data
            
            urlImages = []
            
            try: 
        
                for image in request.FILES.getlist('images'):
                    
                    nombre_imagen = image.name
                    
                    file_extension = nombre_imagen.split(".")[-1]
                    file_path = f"temp/{nombre_imagen}.{file_extension}"
                    
                    default_storage.save(file_path, image)
                    
                    ruta_guardado = f"products/{productName}/{nombre_imagen}"
                    storage.child(ruta_guardado).put(file_path)

                    storage_path = storage.child(ruta_guardado).get_url("2")
        
                    urlImages.append(storage_path)
                    os.remove(file_path)

                optionSale = form.cleaned_data['option']
                
                if optionSale == 'subasta':
                    dataP = {
                        u"title": data['title'],
                        u"description": data['description'],
                        u"urlImages": urlImages,
                        u"price": data['price'],
                        u"stock": data['stock'],
                        u"optionSale": data['option'],
                        u"startingPrice": data['startingPrice'],
                        u"durationDays": data['durationDays'],
                        u"priceCI": data['priceCI']
                        }
                    db.collection('products').document(productName).set(dataP)

                else:
                    dataP = {
                        u"title": data['title'],
                        u"description": data['description'],
                        u"urlImages": urlImages,
                        u"price": data['price'],
                        u"stock": data['stock'],
                        u"optionSale": data['option'],
                        }
                    db.collection('products').document(productName).set(dataP)

                messages.success(request, "Producto guardado correctamente")
                
            except Exception as e:
                
                print(e)
                messages.error(request, "Error al guardar la información")
            
    return render(request, "new_product.html", context)



