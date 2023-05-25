from django import forms

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