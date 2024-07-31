from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "Nom d'utilisateur",widget = forms.TextInput(attrs = {'class':'form-control'}))
    password = forms.CharField(label= 'Mot de passe',widget = forms.PasswordInput(attrs = {'class':'form-control'}))

class RegsiterForm(forms.Form):
    username = forms.CharField(label = "Nom d'utilisateur",widget = forms.TextInput(attrs = {'class':'form-control'}))
    email = forms.CharField(label = "Adresse e-mail",widget = forms.EmailInput(attrs = {'class':'form-control'}) )
    password = forms.CharField(label= 'Mot de passe',widget = forms.PasswordInput(attrs = {'class':'form-control'}))