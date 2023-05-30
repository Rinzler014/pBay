import pyrebase

config = {
  "apiKey": "AIzaSyBXTfsPvXFdUkOWFg1H9f6iYYQpAG7U8xs",
  "authDomain": "pbay-28c3b.firebaseapp.com",
  "databaseURL": "https://pbay-28c3b-default-rtdb.firebaseio.com",
  "projectId": "pbay-28c3b",
  "storageBucket": "pbay-28c3b.appspot.com",
  "serviceAccount": "serAccountKey.json",
  "messagingSenderId": "929831620258",
  "appId": "1:929831620258:web:92775e64330a294b8e11fb",
  "measurementId": "G-TC6V309YST"
}

def noquote(s):
    return s

pyrebase.pyrebase.quote = noquote

firebase = pyrebase.initialize_app(config)

db = firebase.database()

auth = firebase.auth()

storage = firebase.storage()

prods = dict(db.child("products").get().val())
numVendidos = 0

for product_id, product_data in prods.items():
  print(product_id)
  print(product_data)
  
  if product_data["availability"] == "Si":
    numVendidos += 1
  
print(numVendidos)