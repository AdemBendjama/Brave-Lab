from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from .forms import UserRegisterForm
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')