from django.contrib.auth import (
    authenticate, login, update_session_auth_hash
)
from django.contrib.auth.forms import (
    AuthenticationForm ,
    PasswordChangeForm
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect
from brave_lab_project.settings import EMAIL_HOST_USER
from client.models import Client
from .forms import (
   UserRegisterForm, 
   UserUpdateForm, 
   ClientUpdateForm,
   NurseUpdateForm,
   ReceptionistUpdateForm,
   AuditorUpdateForm,
   HomeContactUsForm,
)
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .utils import is_client, is_nurse, is_receptionist, is_auditor

# Create your views here.



@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile_settings')
    else:
        form = PasswordChangeForm(request.user)
        
    group_name = request.user.groups.first().name
        
    return render(request, f'{group_name}/profile/settings.html',{'form':form})


def home(request):
    # Accessing the home page requires log out
    user = request.user
    if user.is_authenticated : 
        if user.is_superuser :
            return redirect('/admin/')
        elif is_client(user) :
            return redirect('client')
        elif is_nurse(user) :
            return redirect('nurse')
        elif is_receptionist(user) :
            return redirect('receptionist')
        elif is_auditor(user) :
            return redirect('auditor')
        
    if request.method == 'POST':
        
        form = HomeContactUsForm(request.POST)
        
        if form.is_valid():
            
            email = form.cleaned_data["email"]
            content = form.cleaned_data["content"]
            
            html = render_to_string('main_home/contact_email_template.html',{
                "email": email,
                'content':content
            })
            
            send_mail("Internet User Support",content ,EMAIL_HOST_USER,["bravelaboratory2023@gmail.com"],html_message=html)
            return redirect('home')
        
    else:
        form = HomeContactUsForm()
        
    context = {
        'form':form,
    }
    
    return render(request,'main_home/home.html',context)



def register(request):
    # Accessing the register page requires log out
    user = request.user
    if user.is_authenticated : 
        if user.is_superuser :
            return redirect('/admin/')
        elif is_client(user) :
            return redirect('client')
        elif is_nurse(user) :
            return redirect('nurse')
        elif is_receptionist(user) :
            return redirect('receptionist')
        elif is_auditor(user) :
            return redirect('auditor')
    
    # handling of a post request from register page
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
    # Accessing the register page requires log out
    user = request.user
    if user.is_authenticated : 
        if user.is_superuser :
            return redirect('/admin/')
        elif is_client(user) :
            return redirect('client')
        elif is_nurse(user) :
            return redirect('nurse')
        elif is_receptionist(user) :
            return redirect('receptionist')
        elif is_auditor(user) :
            return redirect('auditor')
    
    # handling of a post request from register page
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
                elif is_client(user) :
                    return redirect('client')
                elif is_nurse(user) :
                    return redirect('nurse')
                elif is_receptionist(user) :
                    return redirect('receptionist')
                elif is_auditor(user) :
                    return redirect('auditor')
                
    else:
        form = AuthenticationForm()
        
    return render(request, 'main_home/login.html', {'form': form})


@login_required
def profile_update(request):
    
    user = request.user
    
    if request.method == 'POST':
        
        user_form = UserUpdateForm(request.POST, instance=user)
        
        if is_client(user) :
            actor_form = ClientUpdateForm(request.POST, request.FILES, instance=user.client)
        elif is_nurse(user) :
            actor_form = NurseUpdateForm(request.POST, request.FILES, instance=user.nurse)
        elif is_receptionist(user) :
            actor_form = ReceptionistUpdateForm(request.POST, request.FILES, instance=user.receptionist)
        elif is_auditor(user) :
            actor_form = AuditorUpdateForm(request.POST, request.FILES, instance=user.auditor)
        
        if user_form.is_valid() and actor_form.is_valid():
            user_form.save()
            actor_form.save()
            return redirect('profile_update')
        
    else:
        user_form = UserUpdateForm(instance=user)
        
        if is_client(user) :
            actor_form = ClientUpdateForm(instance=user.client)
        elif is_nurse(user) :
            actor_form = NurseUpdateForm(instance=user.nurse)
        elif is_receptionist(user) :
            actor_form = ReceptionistUpdateForm(instance=user.receptionist)
        elif is_auditor(user) :
            actor_form = AuditorUpdateForm(instance=user.auditor)

        
    context={
        "user_form":user_form,
        "actor_form":actor_form,
    }
    
    group_name = user.groups.first().name
    
        
    return render(request, f'{group_name}/profile/profile.html', context)






