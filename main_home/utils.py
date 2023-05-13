from django.contrib.auth.models import Group

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
