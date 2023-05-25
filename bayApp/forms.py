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
    
    name = forms.CharField(widget=forms.widgets.TextInput(attrs={
            'class': 'name-field form-control form-control-lg',
            'placeholder': 'Nombre'
            }))
    
    last_name = forms.CharField(widget=forms.widgets.TextInput(attrs={
            'class': 'name-field form-control form-control-lg',
            'placeholder': 'Apellido Paterno'
            }))
    
    mom_last_name = forms.CharField(widget=forms.widgets.TextInput(attrs={
            'class': 'name-field form-control form-control-lg',
            'placeholder': 'Apellido Materno'
            }))
    
    celluar = forms.CharField(widget=forms.widgets.NumberInput(attrs={
            'class': 'name-field form-control form-control-lg',
            'placeholder': 'Celular',
            }))