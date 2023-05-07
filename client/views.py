from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def client_home(request):
    
    return render(request,'client/client.html')