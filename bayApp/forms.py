from django import forms

class LoginForm(forms.Form):
    
    email = forms.EmailField(widget=forms.widgets.TextInput(attrs={
            'class': 'email-field form-control form-control-lg',
            "placeholder": "Correo Electrónico"}
        ))
    
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={
                'class': 'password-field form-control form-control-lg',
                "placeholder": "Contraseña"}
            ))  
    
    
