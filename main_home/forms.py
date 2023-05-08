from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

phone_regex = RegexValidator(
    regex=r'^0[5-7][0-9]{8}$',
    message='Please enter a valid phone number starting with 05, 06 or 07 and has 10 digits in total'
)
                             
class UserRegisterForm(UserCreationForm):
    
    phone_number = forms.CharField(validators=[phone_regex])
    gender = forms.ChoiceField(choices=((None, 'Choose Here :'),('Male', 'Male'), ('Female', 'Female')))
    address = forms.CharField(max_length=50)
    policy = forms.BooleanField()
    
    phone_number.widget.attrs.update({"placeholder":"+213 0000000000"})
    address.widget.attrs.update({"placeholder":"Setif, El Eulma"})
    
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