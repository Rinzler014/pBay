import pyrebase
# import decouple

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

#The following lines will allow us to acces pbays email
"""from decouple import config

EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('pbaymx@gmail.comL')
EMAIL_HOST_PASSWORD = config('Pbaydelao29')
EMAIL_USE_TLS = True  """

#We create a message template using smpt when we send an email to any user
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_user_mail(user):
    subject = 'Disponibilidad de Producto'
    template = get_template('templates/mi_template_correo.html')

    content = template.render({
        'user': user,
    })

    message = EmailMultiAlternatives(subject, #Titulo
                            ''",
                                    settings.pbaymx@gmail.com, #Remitente
                                    [user.email]) #Destinatario

    message.attach_alternative(content, 'text/html')
    message.send() """ #user.email info will come form the document intrested in our database.

#user = User.objects.last()

#send_user_mail(user)