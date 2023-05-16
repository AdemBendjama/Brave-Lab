from django.shortcuts import render
from django.contrib.auth.decorators import login_required , permission_required

# Create your views here.

################################################################

# Home - Lobby

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def nurse_home(request):
    
    return render(request,'nurse/nurse.html')

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def lobby_detail(request):
    
    return render(request,'nurse/lobby/lobby_detail.html')

################################################################

# Analysis Requests

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_list(request):
    
    return render(request,'nurse/request/request_list.html')

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_detail(request):
    
    return render(request,'nurse/request/request_detail.html')

################################################################

# Analysis Requests Tests

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_add(request):
    
    return render(request,'nurse/request/test/request_test_add.html')

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_list(request):
    
    return render(request,'nurse/request/test/request_test_list.html')

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_detail(request):
    
    return render(request,'nurse/request/test/request_test_detail.html')

################################################################

# Chat

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def message_chat(request):
    
    return render(request,'nurse/message/message_chat.html')