from django.shortcuts import render ,redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required , permission_required

from brave_lab_project.settings import EMAIL_HOST_USER
from .forms import ClientContactForm

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
     
    if request.method == 'POST':
        form = ClientContactForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"]
            send_mail("hello World",content ,EMAIL_HOST_USER,["bravelaboratory2023@gmail.com"])
            return redirect('client')
    else:
        form = ClientContactForm()
        
    context = {
        'form':form,
    }
    
    return render(request,'client/profile/contact.html',context)

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_policy(request):
    
    return render(request,'client/profile/policy.html')

