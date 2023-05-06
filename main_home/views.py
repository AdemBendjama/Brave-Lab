from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'main_home/HomePage.html')


def login(request):
    return render(request,'main_home/LoginPage.html')


def register(request):
    return render(request,'main_home/RegisterPage.html')

def logout(request):
    return render(request,'main_home/Logout.html')