from datetime import date
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from client.models import Client
from main_home.models import BloodBank
from nurse.models import Nurse
from receptionist.models import Receptionist
from auditor.models import Auditor


class HomeContactUsForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))


phone_regex = RegexValidator(
    regex=r'^0[5-7][0-9]{8}$',
    message='Please enter a valid phone number starting with 05, 06 or 07 and has 10 digits in total'
)

class BloodTypeForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.Select)
    blood_type = forms.ChoiceField(choices=BloodBank.BLOOD_TYPES, widget=forms.Select)

    class Meta:
        model = BloodBank
        fields = ['client', 'blood_type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].empty_label = None
        self.fields['client'].initial = Client.objects.first()
                             
class UserRegisterForm(UserCreationForm):
    
    phone_number = forms.CharField(max_length=10,validators=[phone_regex])
    gender = forms.ChoiceField(choices=((None, 'Choose Here :'),('M', 'Male'), ('F', 'Female')))
    address = forms.CharField(max_length=50)
    policy = forms.BooleanField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
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
                  'gender' , 'address' , 'date_of_birth', 'password1' , 'password2', 'policy']
        
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age < 14:
            raise forms.ValidationError("You must be 14 years old or older to register.")
        return date_of_birth
        
        
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        
class ClientUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ['phone_number', 'address', 'profile_pic']
        
class NurseUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Nurse
        fields = ['phone_number', 'address', 'profile_pic']
        
class ReceptionistUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Receptionist
        fields = ['phone_number', 'address', 'profile_pic']

class AuditorUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Auditor
        fields = ['phone_number', 'address', 'profile_pic']


