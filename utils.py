import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin import db

import json


def get_db(collection):

    cred = credentials.Certificate("serAccountKey.json")
    firebase_admin.initialize_app(cred)

    database = firestore.client()
    collection = database.collection('users')
    
    return collection
