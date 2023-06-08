
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User,Group
from django.http import HttpResponse

from main_home.models import BloodBank

def admin_user(request):
    # Get the superuser
    superuser = User.objects.filter(is_superuser=True).first()

    # Get the admin_user group
    admin_group = Group.objects.get(name='admin_user')
                 
    users = User.objects.exclude(pk=superuser.pk).exclude(groups=admin_group).all()
   
    if request.GET.get('date_sort') :
        date = request.GET.get('date')
        
        if date == 'True' :
            users= users.order_by('date_joined')
            sort_date = 'False'
        elif date == "False":
            users= users.order_by('-date_joined')
            sort_date = 'True'
            
        sort_username= request.GET.get('username')
        sort_type= request.GET.get('type')
    
            
    if request.GET.get('username_sort'):
        username = request.GET.get('username')
        
        if username == 'True':
            users = users.order_by("-username")
            sort_username= 'False'
        elif username == 'False':
            users = users.order_by("username")
            sort_username= 'True'
            
        
        sort_date= request.GET.get('date')
        sort_type= request.GET.get('type')
        
    if request.GET.get('type_sort'):
        nurse = request.GET.get('type')
        
        if nurse == 'True':
            users = users.order_by("-groups__name")
            sort_type= 'False'
        elif nurse == 'False':
            users = users.order_by("groups__name")
            sort_type= 'True'
            
        
        sort_date= request.GET.get('date')
        sort_username= request.GET.get('username')
        
            
    if not (request.GET.get('username_sort')) and not (request.GET.get('date_sort')) and not (request.GET.get('type_sort')):
        sort_date = 'True'
        sort_username = 'True'
        sort_type = 'True'
        
    
    if request.method == "POST" and "search" in request.POST :
        search = request.POST.get("search")
        if search != "" :
            try:
                parsed_number = int(search)
                parsable = True
            except ValueError:
                parsable = False
            
            if parsable and users.filter(id=int(search)).exists() :    
                    users = users.filter(id=int(search)).all()
                
            elif users.filter(username=search).exists() :
                users = users.filter(username=search).all()
                
            else :
                context={
                    'sort_username':sort_username,
                    'sort_date':sort_date,
                    'sort_type':sort_type,
                }
                
                return render(request,'auditor/result/result_list.html',context)
    
        
    
    context = {
        'users':users,
        'sort_username':sort_username,
        'sort_date':sort_date,
        'sort_type':sort_type,
    }
    
    return render(request,'admin_user/admin_user.html',context)

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Logic to delete the user
            return redirect('user_delete', user_id=user_id)
        elif 'update' in request.POST:
            # Logic to update the user
            return redirect('user_update', user_id=user_id)

    context = {'user': user}    
    return render(request,'admin_user/users/user_detail.html',context)

def user_delete(request, user_id):
    # Add your logic for the user_delete view here
    user = get_object_or_404(User, id=user_id)  # Assuming you have a User model
    # Delete the user or perform any other necessary actions
    return render(request,'admin_user/users/user_detail.html')

def user_update(request, user_id):
    # Add your logic for the user_update view here
    user = get_object_or_404(User, id=user_id)  # Assuming you have a User model
    # Update the user or perform any other necessary actions
    return render(request,'admin_user/users/user_update.html')

def account_add(request):
    # Add your logic for the account_add view here
    return render(request,'admin_user/accounts/account_add.html')

def account_add_nurse(request):
    # Add your logic for the account_add_nurse view here
    return render(request,'admin_user/accounts/account_add_nurse.html')

def account_add_receptionist(request):
    # Add your logic for the account_add_receptionist view here
    return render(request,'admin_user/accounts/account_add_receptionist.html')

def account_add_auditor(request):
    # Add your logic for the account_add_auditor view here
    return render(request,'admin_user/accounts/account_add_auditor.html')

def blood_banks(request):
    # Add your logic for the blood_banks view here
    return render(request,'admin_user/banks/blood_banks.html')

def blood_bank_detail(request, bank_id):
    # Add your logic for the blood_bank_detail view here
    bank = get_object_or_404(BloodBank, id=bank_id)  # Assuming you have a BloodBank model
    return render(request,'admin_user/banks/blood_bank_detail.html')

def blood_bank_add(request):
    # Add your logic for the blood_bank_add view here
    return render(request,'admin_user/banks/blood_bank_add.html')