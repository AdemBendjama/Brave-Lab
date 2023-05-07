from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib import admin
from django.contrib.auth.models import Group

# Create your views here.

def home(request):
    return render(request,'main_home/home.html')


def register(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            
    else :
        form = UserRegisterForm()
    
    return render(request,'main_home/register.html', {'form':form})


def login_view(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request,user)
                
                if user.is_superuser :
                    return redirect('/admin/')
                
                if is_client(user) :
                        return redirect('client')
                    
                if is_nurse(user) :
                    return redirect('nurse')
                
                if is_receptionist(user) :
                    return redirect('receptionist')
                
                if is_auditor(user) :
                    return redirect('auditor')
                
    else:
        form = AuthenticationForm()
        
    return render(request, 'main_home/login.html', {'form': form})




def is_client(user):
    client_group = Group.objects.get(name='client')
    return client_group in user.groups.all()

def is_nurse(user):
    nurse_group = Group.objects.get(name='nurse')
    return nurse_group in user.groups.all()

def is_receptionist(user):
    receptionist_group = Group.objects.get(name='receptionist')
    return receptionist_group in user.groups.all()

def is_auditor(user):
    auditor_group = Group.objects.get(name='auditor')
    return auditor_group in user.groups.all()