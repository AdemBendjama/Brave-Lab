from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required , permission_required

# Create your views here.

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_home(request):
    
    return render(request,'client/client.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_help(request):
    
    return render(request,'client/profile/help.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_contact(request):
    
    return render(request,'client/profile/contact.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_policy(request):
    
    return render(request,'client/profile/policy.html')

