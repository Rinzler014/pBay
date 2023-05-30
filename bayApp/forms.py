from django import forms
import re
from django.contrib import messages
class LoginForm(forms.Form):
    
    email = forms.EmailField(widget=forms.widgets.TextInput(attrs={
            'class': 'email-field form-control form-control-lg',
            "placeholder": "Email"}
        ))
    
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={
                'class': 'password-field form-control form-control-lg',
                "placeholder": "Password"}
            ))  
    
    
class CacheSignUpFormP1(forms.Form):
    
    name = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nombre'
            }))
    
    last_name = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Apellido Paterno'
            }))
    
    mom_last_name = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Apellido Materno'
            }))
    
    cellular = forms.CharField(required=True,
            widget=forms.widgets.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Celular',
            }))
        
class CacheSignUpFormP2(forms.Form):
    
    country = forms.CharField(required=True,
        widget=forms.widgets.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Pais'
        }))

    state = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Estado'
            }))
    
    city = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ciudad'
            }))
    
    street = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Calle y numero exterior',
            }))
    
    zipcode = forms.CharField(required=True,
            widget=forms.widgets.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Codigo Postal',
            }))
    
    personalID = forms.FileField(required=True,
            widget=forms.widgets.FileInput(attrs={
                'placeholder': 'Identificacion Personal',
            }))


class SignUpForm(forms.Form):
        
    def __init__(self, *args, **kwargs): 
        self.request = kwargs.pop('request')
        super(SignUpForm,self).__init__(*args,**kwargs)
    
    name = forms.CharField(required=True,
        widget=forms.widgets.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Nombre'
        }))
    
    last_name = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Apellido Paterno'
            }))
    
    mom_last_name = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Apellido Materno'
            }))
    
    cellular = forms.CharField(required=True,
            widget=forms.widgets.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Celular',
            }))

    country = forms.CharField(required=True,
        widget=forms.widgets.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Pais'
        }))

    state = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Estado'
            }))
    
    city = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ciudad'
            }))
    
    street = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Calle y numero exterior',
            }))
    
    zipcode = forms.CharField(required=True,
            widget=forms.widgets.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Codigo Postal',
            }))
    
    personalID = forms.CharField(required=True,
            widget=forms.widgets.TextInput(attrs={
                'placeholder': 'Identificacion Personal',
            }))

    email = forms.EmailField(required=True,
            widget=forms.widgets.EmailInput(attrs={
                'class': 'form-input form-control form-control-lg',
                'placeholder': 'Correo Electrónico',
            }))
    
    password = forms.CharField(required=True,
            widget=forms.widgets.PasswordInput(attrs={
                'class': 'form-input pass1 form-control form-control-lg',
                'placeholder': 'Contraseña',
            }))
    
    password2 = forms.CharField(required=True,
            widget=forms.widgets.PasswordInput(attrs={
                'class' : 'form-input pass2 form-control form-control-lg',
                'placeholder': 'Confirma tu contraseña',
            }))
    

    def clean_password2(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            messages.error(self.request, "Las contraseñas no coinciden")
            raise forms.ValidationError("Las contraseñas no coinciden")

        return password2
    
    def clean_password(self):
            
            password = self.cleaned_data.get('password')
            regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
            
            if not regex.match(password):
                messages.error(self.request, "La contraseña debe tener al menos 8 caracteres, una mayuscula, una minuscula, un numero y un caracter especial")
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, una mayuscula, una minuscula, un numero y un caracter especial")
        
            return password

class formNewProduct(forms.Form):
    title = forms.CharField(label='Condición',
        widget=forms.widgets.Textarea(attrs={
        'placeholder': 'Título del producto',
        "cols":"50",
        "rows":"2",
        "resize":"none"
        }))
    condition = forms.CharField(label='Condición',
        widget=forms.widgets.TextInput(attrs={
        'placeholder': 'Condición del producto',
        }))
    brand = forms.CharField(label='Marca',
         widget=forms.widgets.TextInput(attrs={
        'placeholder': 'Marca',
        }))
    material = forms.CharField(label='Material', 
        widget=forms.widgets.TextInput(attrs={
        'placeholder': 'Material',
        }))
    color = forms.CharField(label='Color', 
        widget=forms.widgets.TextInput(attrs={
        'placeholder': 'Color',
        }))
    high = forms.IntegerField(label='Alto', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Alto',
        }))
    width = forms.IntegerField(label='Ancho', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Ancho',
        }))
    long = forms.IntegerField(label='Largo', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Largo',
        }))
    toc = forms.CharField(label='TOC', 
        widget=forms.widgets.TextInput(attrs={
        'placeholder': 'TOC',
        }))
    description = forms.CharField(label='Condición',
        widget=forms.widgets.Textarea(attrs={
        'placeholder': 'Descripción del producto',
        "cols":"50",
        "rows":"5",
        "resize":"none"
        }))
    images = forms.FileField(required=True,
        widget=forms.widgets.FileInput(attrs={
        'placeholder': 'Imágenes del producto',
        }))
    price = forms.IntegerField(label='Largo', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Precio',
        }))
    stock = forms.IntegerField(label='Largo', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Unidades disponibles',
        }))