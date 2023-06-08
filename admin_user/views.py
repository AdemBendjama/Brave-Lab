
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse

from main_home.models import BloodBank

def admin_user(request):
    # Add your logic for the home view here
    return render(request,'admin_user/admin_user.html')

def user_detail(request, user_id):
    # Add your logic for the user_detail view here
    user = get_object_or_404(User, id=user_id)  # Assuming you have a User model
    return render(request,'admin_user/users/user_detail.html')

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