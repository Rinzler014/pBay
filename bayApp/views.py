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
from firebase_admin import auth as Fauth

from django.http import HttpResponse

from datetime import datetime, timedelta

from django.utils import timezone

from django.http import JsonResponse

# Use a service account.
cred = credentials.Certificate("./serAccountKey.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client()


#Login View
def login(request):
    
    #Created a form object to verify the user
    form = LoginForm()
    context = {"form": form}
    
    #Starting the verification process
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            #If the form is valid, we will try to log in the user
            try:
                user = auth.sign_in_with_email_and_password(
                    form.cleaned_data["email"], form.cleaned_data["password"]
                )
                messages.success(
                    request, f"Usuario {user['localId']} autenticado correctamente"
                )
                checkAuctions()
                return redirect("landing", user_id=user["localId"])
            
            #If the user is not found, we will send an error message
            except Exception as e:
                messages.error(request, "Usuario o Contraseña incorrectos")
    return render(request, "login.html", context)

#Signup View First Part
def signup(request):
    
    #Created a form object to request the user's personal information
    form = CacheSignUpFormP1()
    context = {"form": form}

    #Starting the registration process
    if request.method == "POST":
        form = CacheSignUpFormP1(request.POST)
        print(form.is_valid())
        
        #If the form is valid, we will save the user's personal information in the session
        if form.is_valid():
            request.session["personal_info"] = json.dumps(form.cleaned_data)

            return redirect("signup_2")

        return render(request, "signup.html", context)

    return render(request, "signup.html", context)

#Signup View Second Part
def signup_2(request):
    form = CacheSignUpFormP2()
    context = {"form": form}

    #Starting the registration process
    if request.method == "POST":
        form = CacheSignUpFormP2(request.POST, request.FILES)

        #If the form is valid, we will save the user's location information in the session
        if form.is_valid():
            #Saving the user's personal ID in the storage
            file = request.FILES["personalID"]
            file_name = bson.ObjectId()
            file_extension = file.name.split(".")[-1]
            file_path = f"temp/{file_name}.{file_extension}"
            default_storage.save(file_path, file)

            form.cleaned_data["personalID"] = str(file_name) + "." + file_extension

            #Saving the user's profile picture in the storage
            request.session["location_info"] = json.dumps(
                form.cleaned_data, default=str
            )

            return redirect("signup_3")

        return render(request, "signup_2.html", context)

    return render(request, "signup_2.html", context)

#Signup View Third Part
def signup_3(request):
    form = SignUpForm(request=request)
    context = {"form": form}

    #Starting the registration process
    if request.method == "POST":
        
        #If the form is valid, we will update the request data with the user's personal and location information
        personal_info = json.loads(request.session["personal_info"])
        location_info = json.loads(request.session["location_info"])

        updated_data = request.POST.copy()
        updated_data.update(personal_info)
        updated_data.update(location_info)

        #Fill the form with the updated data
        form = SignUpForm(updated_data, request=request)

        #If the form is valid, we will create the user in the database
        if form.is_valid():
            data = form.cleaned_data
            data.pop("password2")

            try:
                
                #Creating the user in the authentication service
                user = auth.create_user_with_email_and_password(
                    data["email"], data["password"]
                )

                data.pop("password")
                data["type"] = "user"

                #Saving the user's personal ID in the storage
                storage.child(f"users/{user['localId']}/personalID").put(
                    f"temp/{data['personalID']}"
                )

                temp_file = data["personalID"]

                data["personalID"] = storage.child(
                    f"users/{user['localId']}/personalID"
                ).get_url(None)


                #Saving the user's information in the database
                db.collection("users").document(user["localId"]).set(data)

                print("Usuario creado correctamente")

                #Deleting the temporary file
                os.remove(f"temp/{temp_file}")

                #Added Cart information to the user
                productos = []

                data = {"UIDUsuario": user["localId"], "Productos": productos}

                db.collection("carritos").add(data)

                #Redirecting the user to the login page
                messages.success(request, f"Usuario creado correctamente")

                return redirect("login")

            #If the user is not created, we will send an error message
            except Exception as e:
                print(e)
                messages.error(request, f"Error al crear usuario: {e}")

    return render(request, "signup_3.html", context)


#Landing View
def landing(request, user_id):
    

    #Retrieve the 10 most sold products 
    queryset = db.collection("products").order_by("totalSales").limit_to_last(10)
    results = queryset.get()
    products = [{product.id: product.to_dict()} for product in results]

    #Retrieve the 10 most stand out products
    queryset2 = db.collection("products").where("standOut", "==", True)
    results2 = queryset2.get()
    products2 = [{product.id: product.to_dict()} for product in results2]

    #Filtering the products to avoid duplicates
    [products.append(product) for product in products2 if product not in products]


    context = {
        "user": user_id,
        "products": products,
    }

    return render(request, "landing.html", context)

#Updating personal info view
def myProfile(request, user_id):
    #We access the document of the user logged in, get the data from the document and make a dict
    docRef = db.collection("users").document(user_id)
    doc = docRef.get()
    initialData = doc.to_dict()

    #We access de personalID image in order to save this only data that can not be updated
    imagen = initialData["personalID"]

    #Declared intial info (already stored info of the user)
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
    
    #We call our form and send the initial data and we create our context that will be sent to the html file
    form = updatePersonalInfo(initial=initial)

    context = {
        "user": user_id,
        "doc": initialData,
        "form": form
    }

    #Start of the form in which we recibe the info with the POST method. After that we make sure that de form is valid
    if request.method == "POST":
        form = updatePersonalInfo(request.POST, request.FILES)
        if form.is_valid():
            #Next up we try to get the data from the form, later we compare if we get an empty data we collect the initial data
            #(previously declared) in order to maintain all the info that will not be updated
            try:
                data = form.cleaned_data
                if data['newName'] == '':
                    data['newName'] = initialData["name"]
                if data['newMomLastName'] == '':
                    data['newMomLastName'] = initialData["mom_last_name"]
                if not data['newPhone'] or not data['newPhone'].isdigit():
                    data['newPhone'] = initialData["cellular"]
                if data['newEmail'] == '':
                    data['newEmail'] = initialData["email"]
                else:
                    Fauth.update_user(user_id, email=data["newEmail"])
                    
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

                #We make the changes of data and we call our document with the user_id and set the data (update all data)
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
                #In case of error we let de user know what caused the system to fail
            except Exception as e:
                print(e)
                messages.error(request, f"Error al crear usuario: {e}")
            
        
            
    return render(request, "my_profile.html", context)

#Update password view
def updatePassword(request):
    #Simply we just get the user_id sent from de data from the html with an ajax function. We get de ref of the doc and extract only
    #the email of the user
    user_id = request.GET.get('idUsuario')

    docRef = db.collection("users").document(user_id).get()

    doc = docRef.to_dict()

    email = doc["email"]

    #Sends an email to the current registered email in order to change the current password of the user
    auth.send_password_reset_email(email)

    return HttpResponse(status=200)



def edit_info_prod(request, user_id, product_id):
    productID = product_id
    doc_ref = db.collection("products").document(productID)
    doc = doc_ref.get()
    initialData = doc.to_dict()

    # Se decide si el objeto a cambiar es una subasta o no para obtener la información
    if initialData["optionSale"] == "subasta":
        initial = {
            "title": initialData["title"],
            "description": initialData["description"],
            "stock": initialData["stock"],
            "price": initialData["price"],
        }
    else:
        initial = {
            "title": initialData["title"],
            "description": initialData["description"],
            "price": initialData["price"],
            "stock": initialData["stock"],
        }

    # Se llama al formulario enviando un diccionario con la información que se obtuvo
    # de la base de datos
    form = formEditInfoProduct(initial=initial)

    context = {
        "user": user_id,
        "product": productID,
        "form": form,
    }

    # En caso de que sí se haya enviado algo, se entra a estas líneas
    if request.method == "POST":
        form = formEditInfoProduct(request.POST, request.FILES)

        # Sólo se entrará a las siguientes líenas si el formulario se envió de
        # forma adecuada
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            file = request.FILES["images"]
            file_name = bson.ObjectId()
            file_extension = file.name.split(".")[-1]
            file_path = f"temp/{file_name}.{file_extension}"
            default_storage.save(file_path, file)

            storage.child(f"products/{productID}/{file_name}").put(file_path)

            urlImages = []

            # Se procesan y suben las imágenes que se hayan ingresado al formulario
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

            ## Se actualiza la información enviando los datos obtenidos del formulario
            dataP = {
                "title": data['title'],
                "description": data['description'],
                "urlImages": urlImages,
                "stock": data['stock'],
                "price": data['price'],
                "category": data["category"],
                "subcategory": subcategoryLabel,
                }
            db.collection('products').document(productID).update(dataP)
            
            return redirect("my_products", user_id=user_id)
            
    return render(request, "edit_info_prod.html", context)


def details(request, user_id, product_id):
    prodDetails = db.collection("products").document(product_id).get().to_dict()
    context = {"user": user_id, "prodDetails": prodDetails, "producto_id": product_id}

    return render(request, "details_prod.html", context)

#Adding one more of a product to shopping cart view
def addProductShoppingCart(request):
    #We recieve the product and user ID in order to get the documents needed
    idProducto = request.GET.get("idProducto")
    idUsuario = request.GET.get("idUsuario")

    #We get the shopping cart linked to our current user
    docShoppingCart = (
        db.collection("carritos").where("UIDUsuario", "==", idUsuario).get()
    )

    #We get the ID of the shopping cart and get all the data from it and we assign our array of products from the database to a variable
    for doc in docShoppingCart:
        docID = doc.id

    docs = db.collection("carritos").document(docID)
    doc = docs.get()

    datos = doc.to_dict()

    products = datos["Productos"]

    #We add the same product to the shopping cart and update the data of the shopping cart in the database
    products.append(idProducto)

    data = {"UIDUsuario": idUsuario, "Productos": products}

    db.collection("carritos").document(docID).set(data)
    messages.success(request, "Producto agregado al carrito")

    return HttpResponse(status=200)

#Erasing one more of a product to shopping cart view
def eraseProductShoppingCart(request):
    #We recieve the product and user ID in order to get the documents needed
    idProducto = request.GET.get("idProducto")
    idUsuario = request.GET.get("idUsuario")

    #We get the shopping cart linked to our current user
    docShoppingCart = (
        db.collection("carritos").where("UIDUsuario", "==", idUsuario).get()
    )

    #We get the ID of the shopping cart and get all the data from it and we assign our array of products from the database to a variable
    for doc in docShoppingCart:
        docID = doc.id

    docs = db.collection("carritos").document(docID)
    doc = docs.get()

    datos = doc.to_dict()

    products = datos["Productos"]

    #We look for the product in the list of products, if we find it we erase one of it
    n = 0
    while n != len(products):
        if idProducto == products[n]:
            del products[n]
            break
        else:
            n += 1

    #We save the data into the database again
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

#Pulling info to the shopping cart view
def shopping_cart(request, user_id):
    #We access to the shopping cart of the current user logged in
    docShoppingCart = (
        db.collection("carritos").where("UIDUsuario", "==", user_id).stream()
    )

    #We get the id of the doc of the corresponding shopping cart
    docID = ""
    for doc in docShoppingCart:
        docID = doc.id

    #Array that will contain the products in the shopping cart
    arrayProducts = []

    #We get the data of the document of the shopping cart and make it a dict and we assign the array of products to a variable
    docs = db.collection("carritos").document(docID)
    doc = docs.get()

    datos = doc.to_dict()

    products = datos["Productos"]

    #For cycle that passes all products in the array of products
    for product in products:
        #This while cyclye counts how many times the product is in the shopping cart
        n = 0
        totalProductoNum = 0
        while n != len(products):
            if product == products[n]:
                totalProductoNum += 1
            n += 1

        #We get the document of the product in order to get all the info of the product 
        docs = db.collection("products").document(product)
        doc = docs.get()
        datos = doc.to_dict()
        #We get the first image of the product to show it in the shopping cart
        firstImageProduct = datos["urlImages"]
        imgProduct = firstImageProduct[0]
        #We create our object of product using the information of the product in the database
        productObject = pr(
            id=product,
            nameModel=datos["title"],
            descriptionModel=datos["description"],
            priceModel=datos["price"],
            imgModel=imgProduct,
            totalProductModel=totalProductoNum,
        )

        #We check if we are nos repeating products in the list that will be cycled in the for of
        #the html in order to show the products in the shopping cart
        if productObject not in arrayProducts:
            arrayProducts.append(productObject)

    #In this for cycle we just get the final price of all the products and the final amount of products
    totalShoppingCartProducts = 0
    totalShoppingCartPrice = 0

    for product in arrayProducts:
        totalShoppingCartPrice += product.priceModel * product.totalProductModel
        totalShoppingCartProducts += product.totalProductModel

    #We send the data to the html file
    context = {
        "arrayProducts": arrayProducts,
        "user": user_id,
        "totalShoppingCartPrice": totalShoppingCartPrice,
        "totalShoppingCartProducts": totalShoppingCartProducts,
    }


    return render(request, "shopping_cart.html", context)

#System Auctions View
def auctions(request, user_id):
    
    #Retrieve all system auctions
    platform_bids = db.collection("subasta").stream()

    #Create a list of dictionaries with the auctions
    bids = [{bid.id: bid.to_dict()} for bid in platform_bids]

    context = {
        "user": user_id,
        "bids": bids,
    }

    return render(request, "bids.html", context)


#User´s bids view
def bids_state(request, user_id):
    
    #Retrieve all bids and auctions that user has participated in
    user_bids = db.collection("users").document(user_id).collection("bids").stream()

    #Create a list of dictionaries with the bids
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

    if search_name and len(search_name) >= 3:
        # Convierte el término de búsqueda en una expresión regular, ignorando mayúsculas y minúsculas
        regex = re.compile(search_name, re.IGNORECASE)
        
        platform_products = db.collection("products").where("title", ">", "").stream()
        products = [{product.id : product.to_dict()} for product in platform_products if regex.search(product.to_dict()["title"])]
    else:
        products = []

    
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


def get_product_suggestions(request):
    search_term = request.GET.get('q')

    if search_term and len(search_term) >= 3:
        regex = re.compile(search_term, re.IGNORECASE)
        
        platform_products = db.collection("products").where("title", ">", "").stream()
        product_suggestions = [product.to_dict()["title"] for product in platform_products if regex.search(product.to_dict()["title"])]
    else:
        product_suggestions = []

    data = {
        'suggestions': product_suggestions
    }

    return JsonResponse(data)

## Function to check if the auctions are still available
def checkAuctions():
    col = db.collection("products").stream()

    # Iteration across all the products list
    for document in col:
        dic = document.to_dict()

        # Check if the product is an auction and if it is still available
        if dic["optionSale"] == "subasta" and dic["auctionAvailable"]:
            date = timezone.now()

            # Check if the deletion date is less than the current date
            if date > dic["deletionDate"]:
                docId = document.id
                # Changes the auctionAvailable value to False
                db.collection("products").document(docId).update(
                    {"auctionAvailable": False}
                )
