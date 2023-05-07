from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib import admin

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
                else :
                    return redirect('client')
                
    else:
        form = AuthenticationForm()
        
    return render(request, 'main_home/login.html', {'form': form})
