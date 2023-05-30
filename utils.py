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

db.child("auctions").child("auction4").set({
  "product_key": "product4",
  "user_key": "user1",
  "highest_bid": "5000",
  "remaining_time": "50 Minutes",
  "state": "active",
  "start_price": "1000"
})

