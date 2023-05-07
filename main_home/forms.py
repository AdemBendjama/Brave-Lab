from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
                             
class UserRegisterForm(UserCreationForm):
    
    phone_number = forms.IntegerField(widget = forms.NumberInput(attrs={'placeholder': '+213 0000000000'}))
    gender = forms.ChoiceField(choices=((None, 'Choose Here :'),('Male', 'Male'), ('Female', 'Female')))
    address = forms.CharField(max_length=50,widget = forms.TextInput(attrs={'placeholder': 'Setif, El Eulma'}))
    policy = forms.BooleanField()
    
    
    class Meta():
        model = User
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder': 'ahmed'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ahmed.amokrane@gmail.com'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
        }
        fields = ['username','email','first_name', 'last_name' , 'phone_number',
                  'gender' , 'address' , 'password1' , 'password2', 'policy']
        
        
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)