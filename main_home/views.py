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
