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
    
    
    def clean(self):
        
        cleaned_data = super().clean()
        
        password = self.cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$')
        
        if not regex.match(password):
            messages.error(self.request, "La contraseña debe tener al menos 8 caracteres, una mayuscula, una minuscula, un numero y un caracter especial")
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, una mayuscula, una minuscula, un numero y un caracter especial")
        
        if password != password2:
            messages.error(self.request, "Las contraseñas no coinciden")
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data
    

class formNewProduct(forms.Form):
    title = forms.CharField(label='Condición',
        widget=forms.widgets.Textarea(attrs={
        'placeholder': 'Título del producto',
        "cols":"50",
        "rows":"2",
        "resize":"none"
        }))
    description = forms.CharField(label='Condición',
        widget=forms.widgets.Textarea(attrs={
        'placeholder': 'Descripción del producto',
        "cols":"50",
        "rows":"5",
        "resize":"none"
        }))
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    price = forms.IntegerField(label='Largo', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Precio',
        }))
    stock = forms.IntegerField(label='Largo', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Unidades disponibles',
        }))
    option = forms.ChoiceField(label='Opción', choices=[('venta_directa', 'Venta Directa'), ('subasta', 'Subasta')], widget=forms.RadioSelect)
    category = forms.ChoiceField(label='Categoria', choices=[('tecnologia', 'Tecnologia'), ('entretenimiento', 'Entretenimiento'), ('vehiculos', 'Vehiculos'), ('muebles', 'Muebles'), ('vestimenta', 'Vestimenta'), ('otros', 'Otros')])
    technology = forms.ChoiceField(label='Tecnologia', choices=[('computadoras', 'Computadoras'), ('microondas', 'Microondas'), ('televisiones', 'Televisiones'), ('telefonos', 'Telefonos'), ('mouse', 'Mouse'), ('otros', 'Otros')])
    entertainment = forms.ChoiceField(label='Entretenimiento', choices=[('peliculas', 'Peliculas'), ('videojuegos', 'Videojuegos'), ('personal', 'Entretenimiento Personal'), ('musica', 'Musica'), ('deportes', 'Deportes'), ('otros', 'Otros')])
    vehicles = forms.ChoiceField(label='Vehiculos', choices=[('motos', 'Motocicletas'), ('coches', 'Coches'), ('aviones', 'Aviones'), ('camiones', 'Camiones'), ('bicicletas', 'Bicicletas'), ('otros', 'Otros')])
    furniture = forms.ChoiceField(label='Muebles', choices=[('sillas', 'Sillas'), ('mesas', 'Mesas'), ('camas', 'Camas'), ('sofas', 'Sofas'), ('cajones', 'Cajones'), ('otros', 'Otros')])
    clothing = forms.ChoiceField(label='Vestimenta', choices=[('vestidos', 'Vestidos'), ('pantalones', 'Pantalones'), ('accesorios', 'Accesorios'), ('playeras', 'Playeras'), ('abrigos', 'Abrigos'), ('otros', 'Otros')])
    standOut = forms.BooleanField(required=False)
    startingPrice = forms.IntegerField(label='Campo Adicional 1', required=False, 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Precio de Inicio'
        }))
    durationDays = forms.IntegerField(label='Campo Adicional 2', required=False, 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Duración en días'
        }))
    priceCI = forms.IntegerField(label='Campo Adicional 3', required=False, 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Precio de C/I'
        }))
        
class formEditInfoProduct(forms.Form):
    title = forms.CharField(label='Condición',
        widget=forms.widgets.Textarea(attrs={
        'placeholder': 'Título del producto',
        "cols":"50",
        "rows":"2",
        "resize":"none",
        }))
    description = forms.CharField(label='Condición',
        widget=forms.widgets.Textarea(attrs={
        'placeholder': 'Descripción del producto',
        "cols":"50",
        "rows":"5",
        "resize":"none"
        }))
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    price = forms.IntegerField(label='Largo', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Precio',
        }))
    stock = forms.IntegerField(label='Largo', 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Unidades disponibles',
        }))
    directSale = forms.BooleanField(label='Venta Directa', required=False,
        widget=forms.widgets.CheckboxInput(attrs={
        'placeholder': 'Venta Directa',
        }))
    auction = forms.BooleanField(label='Subasta', required=False, 
        widget=forms.widgets.CheckboxInput(attrs={
        'placeholder': 'Venta Directa',
        }))
    #option = forms.ChoiceField(label='Opción', choices=[('venta_directa', 'Venta Directa'), ('subasta', 'Subasta')], widget=forms.RadioSelect)
    startingPrice = forms.IntegerField(label='Campo Adicional 1', required=False, 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Precio de Inicio',
        }))
    durationDays = forms.IntegerField(label='Campo Adicional 2', required=False, 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Duración en días',
        }))
    priceCI = forms.IntegerField(label='Campo Adicional 3', required=False, 
        widget=forms.widgets.NumberInput(attrs={
        'placeholder': 'Precio de C/I',
        }))
    category = forms.ChoiceField(label='Categoria', choices=[('tecnologia', 'Tecnologia'), ('entretenimiento', 'Entretenimiento'), ('vehiculos', 'Vehiculos'), ('muebles', 'Muebles'), ('vestimenta', 'Vestimenta'), ('otros', 'Otros')])
    technology = forms.ChoiceField(label='Tecnologia', choices=[('computadoras', 'Computadoras'), ('microondas', 'Microondas'), ('televisiones', 'Televisiones'), ('telefonos', 'Telefonos'), ('mouse', 'Mouse'), ('otros', 'Otros')])
    entertainment = forms.ChoiceField(label='Entretenimiento', choices=[('peliculas', 'Peliculas'), ('videojuegos', 'Videojuegos'), ('personal', 'Entretenimiento Personal'), ('musica', 'Musica'), ('deportes', 'Deportes'), ('otros', 'Otros')])
    vehicles = forms.ChoiceField(label='Vehiculos', choices=[('motos', 'Motocicletas'), ('coches', 'Coches'), ('aviones', 'Aviones'), ('camiones', 'Camiones'), ('bicicletas', 'Bicicletas'), ('otros', 'Otros')])
    furniture = forms.ChoiceField(label='Muebles', choices=[('sillas', 'Sillas'), ('mesas', 'Mesas'), ('camas', 'Camas'), ('sofas', 'Sofas'), ('cajones', 'Cajones'), ('otros', 'Otros')])
    clothing = forms.ChoiceField(label='Vestimenta', choices=[('vestidos', 'Vestidos'), ('pantalones', 'Pantalones'), ('accesorios', 'Accesorios'), ('playeras', 'Playeras'), ('abrigos', 'Abrigos'), ('otros', 'Otros')])
    
class updatePersonalInfo(forms.Form):
    newName = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nuevo nombre',
    }))
    newMomLastName = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nuevo Apellido Materno',
    }))
    newPhone = forms.CharField(required=False, widget=forms.widgets.NumberInput(attrs={
    'placeholder': 'Nuevo celular',
    }))
    newEmail = forms.EmailField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nuevo correo',
    }))
    newPassword = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nueva contraseña',
    }))
    newLastName = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nuevo Apellido Paterno',
    }))
    newZipCode = forms.CharField(required=False, widget=forms.widgets.NumberInput(attrs={
    'placeholder': 'Nuevo Código Postal',
    }))
    newStreet = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nueva calle',
    }))
    newState = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nuevo estado',
    }))
    newCountry = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={
    'placeholder': 'Nuevo País',
    }))
