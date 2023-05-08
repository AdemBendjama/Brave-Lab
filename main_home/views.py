from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib import admin
from django.contrib.auth.models import Group
from client.models import Client

# Create your views here.

def home(request):
    return render(request,'main_home/home.html')


def register(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Automaticly save the client and add him to the client group
            # save the user into the user database
            user = form.save()
            # add him to the client group
            group = Group.objects.get(name="client")
            group.user_set.add(user)
            # extract form data
            data = form.cleaned_data
            phone_number = data.get("phone_number")
            gender = data.get("gender")
            address = data.get("address")
            policy = data.get("policy")
            # add him with any additionel information into the client table
            Client.objects.create(user = user,
                            phone_number = phone_number,
                            gender = gender,
                            address = address,
                            policy = policy)
            
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