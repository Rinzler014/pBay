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


firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

storage = firebase.storage()

#Get image from firebase storage

print(storage.child("users/4K0Q36jhUtORhc0eiaMAYMCw2CE3/personalID").get_url("2"))
