from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import *
from utils import *
import json
import bson
from django.core.files.storage import FileSystemStorage, default_storage
import os
from .models import producto as pr
from django.http import HttpResponseRedirect
from django.urls import reverse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from django.http import HttpResponse

from datetime import datetime, timedelta

from django.utils import timezone


# Use a service account.
cred = credentials.Certificate("./serAccountKey.json")

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
                checkAuctions()
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

    if request.method == "POST":
        personal_info = json.loads(request.session["personal_info"])
        location_info = json.loads(request.session["location_info"])

        updated_data = request.POST.copy()
        updated_data.update(personal_info)
        updated_data.update(location_info)

        form = SignUpForm(updated_data, request=request)

        if form.is_valid():
            data = form.cleaned_data
            data.pop("password2")

            try:
                user = auth.create_user_with_email_and_password(
                    data["email"], data["password"]
                )

                data.pop("password")
                data["type"] = "user"

                storage.child(f"users/{user['localId']}/personalID").put(
                    f"temp/{data['personalID']}"
                )

                temp_file = data["personalID"]

                data["personalID"] = storage.child(
                    f"users/{user['localId']}/personalID"
                ).get_url(None)

                db.collection("users").document(user["localId"]).set(data)

                print("Usuario creado correctamente")

                os.remove(f"temp/{temp_file}")

                productos = []

                data = {"UIDUsuario": user["localId"], "Productos": productos}

                db.collection("carritos").add(data)

                messages.success(request, f"Usuario creado correctamente")

                return redirect("login")

            except Exception as e:
                print(e)
                messages.error(request, f"Error al crear usuario: {e}")

    return render(request, "signup_3.html", context)


def landing(request, user_id):
    queryset = db.collection("products").order_by("totalSales").limit_to_last(10)
    results = queryset.get()
    products = [{product.id: product.to_dict()} for product in results]

    context = {
        "user": user_id,
        "products": products,
    }

    return render(request, "landing.html", context)


def myProfile(request, user_id):
    docRef = db.collection("users").document(user_id)

    doc = docRef.get()

    initialData = doc.to_dict()

    imagen = initialData["personalID"]

    initial = {
            "name": initialData["name"],
            "mom_last_name": initialData["mom_last_name"],
            "phone": initialData["cellular"],
            "email": initialData["email"],
            "last_name": initialData["last_name"],
            "zipcode": initialData["zipcode"],
            "street": initialData["street"],
            "state": initialData["state"],
            "country": initialData["country"],
            #"option": initialData["optionSale"]
        }
    
    form = updatePersonalInfo(initial=initial)

    context = {
        "user": user_id,
        "doc": initialData,
        "form": form
    }

    
    

    if request.method == "POST":
        form = updatePersonalInfo(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if data['newName'] == '':
                data['newName'] = initialData["name"]
            if data['newMomLastName'] == '':
                data['newMomLastName'] = initialData["mom_last_name"]
            if not data['newPhone'] or not data['newPhone'].isdigit():
                data['newPhone'] = initialData["cellular"]
            if data['newEmail'] == '':
                data['newEmail'] = initialData["email"]
            """ if data['newPassword'] != '':
                auth.update_profile(user_id, password = data['newPassword']) """
            if data['newLastName'] == '':
                data['newLastName'] = initialData["last_name"]
            if not data['newZipCode'] or not['newZipCode'].isdigit():
                data['newZipCode'] = initialData["zipcode"]
            if data['newStreet'] == '':
                data['newStreet'] = initialData["street"]
            if data['newState'] == '':
                data['newState'] = initialData["state"]
            if data['newCountry'] == '':
                data['newCountry'] = initialData["country"]

            dataP = {
                u"name": data['newName'],
                u"mom_last_name": data['newMomLastName'],
                u"cellular": data['newPhone'],
                u"email": data['newEmail'],
                u"last_name": data['newLastName'],
                u"zipcode": data['newZipCode'],
                u"personalID" : imagen,
                u"street": data['newStreet'],
                u"state": data['newState'],
                u"country": data['newCountry'],
                }
            db.collection('users').document(user_id).set(dataP)
        
            
    return render(request, "my_profile.html", context)

def edit_info_prod(request, user_id, product_id):
    productID = product_id
    doc_ref = db.collection("products").document(productID)
    doc = doc_ref.get()
    initialData = doc.to_dict()

    if initialData["optionSale"] == "subasta":
        initial = {
            "title": initialData["title"],
            "description": initialData["description"],
            "price": initialData["price"],
            "stock": initialData["stock"],
            "totalSales": initialData["totalSales"],
            "startingPrice": initialData["startingPrice"],
            "durationDays": initialData["durationDays"],
            "priceCI": initialData["priceCI"],
            # "option": initialData["optionSale"]
        }
    else:
        initial = {
            "title": initialData["title"],
            "description": initialData["description"],
            "price": initialData["price"],
            "stock": initialData["stock"],
            "totalSales": initialData["totalSales"],
            # "option": initialData["optionSale"]
        }

    form = formEditInfoProduct(initial=initial)

    context = {
        "user": user_id,
        "product": productID,
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

            for image in request.FILES.getlist("images"):
                nombre_imagen = image.name

                file_extension = nombre_imagen.split(".")[-1]
                file_path = f"temp/{nombre_imagen}.{file_extension}"

                default_storage.save(file_path, image)

                ruta_guardado = f"products/{productID}/{nombre_imagen}"
                storage.child(ruta_guardado).put(file_path)

                storage_path = storage.child(ruta_guardado).get_url("2")

                urlImages.append(storage_path)
                os.remove(file_path)

            optionSale = form.cleaned_data["option"]

            if optionSale == "subasta":
                dataP = {
<<<<<<< HEAD
                    "title": data["title"],
                    "description": data["description"],
                    "urlImages": urlImages,
                    "price": data["price"],
                    "stock": data["stock"],
                    "totalSales": data["totalSales"],
                    "optionSale": data["option"],
                    "startingPrice": data["startingPrice"],
                    "durationDays": data["durationDays"],
                    "priceCI": data["priceCI"],
                }
                db.collection("products").document(productID).set(dataP)

            else:
                dataP = {
                    "title": data["title"],
                    "description": data["description"],
                    "urlImages": urlImages,
                    "price": data["price"],
                    "stock": data["stock"],
                    "totalSales": data["totalSales"],
                    "optionSale": data["option"],
                }
                db.collection("products").document(productID).set(dataP)
=======
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
                db.collection('products').document(productID).update(dataP)

            else:
                dataP = {
                    u"title": data['title'],
                    u"description": data['description'],
                    u"urlImages": urlImages,
                    u"price": data['price'],
                    u"stock": data['stock'],
                    u"optionSale": data['option'],
                    }
                db.collection('products').document(productID).update(dataP)
            
>>>>>>> main

    return render(request, "edit_info_prod.html", context)


def details(request, user_id, product_id):
    prodDetails = db.collection("products").document(product_id).get().to_dict()
    context = {"user": user_id, "prodDetails": prodDetails, "producto_id": product_id}

    return render(request, "details_prod.html", context)


def addProductShoppingCart(request):
    idProducto = request.GET.get("idProducto")
    idUsuario = request.GET.get("idUsuario")

    docShoppingCart = (
        db.collection("carritos").where("UIDUsuario", "==", idUsuario).get()
    )

    for doc in docShoppingCart:
        docID = doc.id

    docs = db.collection("carritos").document(docID)
    doc = docs.get()

    datos = doc.to_dict()

    products = datos["Productos"]

    products.append(idProducto)

    data = {"UIDUsuario": idUsuario, "Productos": products}

    db.collection("carritos").document(docID).set(data)
    messages.success(request, "Producto agregado al carrito")

    return HttpResponse(status=200)


def eraseProductShoppingCart(request):
    idProducto = request.GET.get("idProducto")
    idUsuario = request.GET.get("idUsuario")

    docShoppingCart = (
        db.collection("carritos").where("UIDUsuario", "==", idUsuario).get()
    )

    for doc in docShoppingCart:
        docID = doc.id

    docs = db.collection("carritos").document(docID)
    doc = docs.get()

    datos = doc.to_dict()

    products = datos["Productos"]

    print(products)

    n = 0
    while n != len(products):
        if idProducto == products[n]:
            del products[n]
            break
        else:
            n += 1

    print(products)

    data = {"UIDUsuario": idUsuario, "Productos": products}

    db.collection("carritos").document(docID).set(data)

    return HttpResponse(status=200)


def sales(request, user):
    prods = [prod.to_dict() for prod in db.collection("products").get()]
    prod_id = [prod.id for prod in db.collection("products").get()]

    for prod in prods:
        prod["product_id"] = prod_id[0]
        prod_id.pop(0)

    num_vendidos = 0

    nonum_vendidos = 0
    for product_data in prods:
        if product_data["stock"] > 0:
            num_vendidos += 1

    nonum_vendidos = 0

    for product_data in prods:
        if product_data["stock"] <= 0:
            nonum_vendidos += 1

    totalSales = 0

    for product_data in prods:
        if product_data["totalSales"] != 0:
            totalSales += product_data["totalSales"]

    tot_ventas = 0
    subtot = 0

    for product_data in prods:
        if product_data["price"] != 0 and product_data["totalSales"] != 0:
            subtot += product_data["price"] * product_data["totalSales"]
            tot_ventas += subtot

    prod_list = []
    for product_data in prods:
        if product_data["stock"] > 0 and product_data["totalSales"] != 0:
            prod_list.append(product_data)

    noprod_list = []
    for product_data in prods:
        if product_data["stock"] <= 0 and product_data["totalSales"] != 0:
            noprod_list.append(product_data)
    context = {
        "user": user,
        "num_vendidos": num_vendidos,
        "context_list": prod_list,
        "nocontext_list": noprod_list,
        "nonum_vendidos": nonum_vendidos,
        "totalSales": totalSales,
        "tot_ventas": tot_ventas,
    }

    return render(request, "sales.html", context)


def shopping_cart(request, user_id):
    docShoppingCart = (
        db.collection("carritos").where("UIDUsuario", "==", user_id).stream()
    )

    docID = ""
    for doc in docShoppingCart:
        docID = doc.id

    arrayProducts = []

    docs = db.collection("carritos").document(docID)
    doc = docs.get()

    datos = doc.to_dict()

    products = datos["Productos"]

    for product in products:
        n = 0
        totalProductoNum = 0
        while n != len(products):
            if product == products[n]:
                totalProductoNum += 1
            n += 1

        docs = db.collection("products").document(product)
        doc = docs.get()

        prue = datos["urlImages"]
        imgPro = storage.child(prue[0]).get_url("2")
        productObject = pr(
            id=product,
            nameModel=datos["title"],
            descriptionModel=datos["description"],
            priceModel=datos["price"],
            imgModel=imgPro,
            totalProductModel=totalProductoNum,
        )

        if productObject not in arrayProducts:
            arrayProducts.append(productObject)

    totalShoppingCartProducts = 0
    totalShoppingCartPrice = 0

    for product in arrayProducts:
        totalShoppingCartPrice += product.priceModel * product.totalProductModel
        totalShoppingCartProducts += product.totalProductModel

    context = {
        "arrayProducts": arrayProducts,
        "user": user_id,
        "totalShoppingCartPrice": totalShoppingCartPrice,
        "totalShoppingCartProducts": totalShoppingCartProducts,
    }


    return render(request, "shopping_cart.html", context)


def auctions(request, user_id):
    platform_bids = db.collection("subasta").stream()

    bids = [{bid.id: bid.to_dict()} for bid in platform_bids]

    context = {
        "user": user_id,
        "bids": bids,
    }

    return render(request, "bids.html", context)


def bids_state(request, user_id):
    user_bids = db.collection("users").document(user_id).collection("bids").stream()

    bids = [{bid.id: bid.to_dict()} for bid in user_bids]

    context = {
        "user": user_id,
        "bids": bids,
    }

    return render(request, "bids_state.html", context)


def my_products(request, user_id):
    platform_products = (
        db.collection("products").where("sellerID", "==", user_id).stream()
    )
    products = [{product.id: product.to_dict()} for product in platform_products]

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
                for image in request.FILES.getlist("images"):
                    nombre_imagen = image.name

                    file_extension = nombre_imagen.split(".")[-1]
                    file_path = f"temp/{nombre_imagen}.{file_extension}"

                    default_storage.save(file_path, image)

                    ruta_guardado = f"products/{productName}/{nombre_imagen}"
                    storage.child(ruta_guardado).put(file_path)

                    storage_path = storage.child(ruta_guardado).get_url("2")

                    urlImages.append(storage_path)
                    os.remove(file_path)

                optionSale = form.cleaned_data["option"]
                subcategories = {
                    "tecnologia": "technology",
                    "entretenimiento": "entertainment",
                    "vehiculos": "vehicles",
                    "muebles": "furniture",
                    "vestimenta": "clothing",
                }
                subcategoryLabel = ""
                if data["category"] == "otros":
                    subcategoryLabel = None
                else:
                    subcategoryLabel = data[subcategories[data["category"]]]
                if optionSale == "subasta":
                    creationDate = datetime.now()
                    deletionDate = creationDate + timedelta(days=data["durationDays"])
                    print(deletionDate)
                    dataP = {
                        "title": data["title"],
                        "description": data["description"],
                        "urlImages": urlImages,
                        "price": data["price"],
                        "stock": data["stock"],
                        "totalSales": 0,
                        "optionSale": data["option"],
                        "standOut": data["standOut"],
                        "startingPrice": data["startingPrice"],
                        "durationDays": data["durationDays"],
                        "priceCI": data["priceCI"],
                        "auctionAvailable": True,
                        "deletionDate": deletionDate,
                        "sellerID": user_id,
                        "category": data["category"],
                        "subcategory": subcategoryLabel,
                    }
                    db.collection("products").document(productName).set(dataP)

                if optionSale == "venta_directa":
                    dataP = {
                        "title": data["title"],
                        "description": data["description"],
                        "urlImages": urlImages,
                        "price": data["price"],
                        "stock": data["stock"],
                        "totalSales": 0,
                        "optionSale": data["option"],
                        "standOut": data["standOut"],
                        "sellerID": user_id,
                        "category": data["category"],
                        "subcategory": subcategoryLabel,
                    }
                    db.collection("products").document(productName).set(dataP)

                messages.success(request, "Producto guardado correctamente")

            except Exception as e:
                print(e)
                messages.error(request, "Error al guardar la información")

    return render(request, "new_product.html", context)


def search_products(request, user_id):
    search_name = request.GET.get("q")

    categories = [
        "tecnologia",
        "entretenimiento",
        "vehiculos",
        "muebles",
        "vestimenta",
        "otros",
    ]

    subcategories = [
        "computadoras",
        "microondas",
        "televisiones",
        "telefonos",
        "mouse",
        "peliculas",
        "videojuegos",
        "personal",
        "musica",
        "deportes",
        "motos",
        "coches",
        "aviones",
        "camiones",
        "bicicletas",
        "sillas",
        "mesas",
        "camas",
        "sofas",
        "cajones",
        "vestidos",
        "pantalones",
        "accesorios",
        "playeras",
        "abrigos",
    ]

    platform_products = (
        db.collection("products").where("title", "==", search_name).stream()
    )
    products = [{product.id: product.to_dict()} for product in platform_products]

    if not products and search_name in subcategories:
        platform_products = (
            db.collection("products").where("subcategory", "==", search_name).stream()
        )
        products = [{product.id: product.to_dict()} for product in platform_products]
    elif not products and search_name in categories:
        platform_products = (
            db.collection("products").where("category", "==", search_name).stream()
        )
        products = [{product.id: product.to_dict()} for product in platform_products]

    context = {
        "user": user_id,
        "products": products,
        "search_name": search_name,
    }

    return render(request, "search_results.html", context)


def checkAuctions():
    col = db.collection("products").stream()

    for document in col:
        dic = document.to_dict()

        if dic["optionSale"] == "subasta" and dic["auctionAvailable"]:
            date = timezone.now()

            if date > dic["deletionDate"]:
                docId = document.id
                db.collection("products").document(docId).update(
                    {"auctionAvailable": False}
                )
