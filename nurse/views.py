from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required , permission_required
from main_home.models import AnalysisRequest, Appointment, Lobby

from nurse.models import Nurse

# Create your views here.

################################################################

# Home - Lobby

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def nurse_home(request):
    nurse = request.user.nurse
    lobby = nurse.lobby
    clients = lobby.clients.all()

    context = {
        'nurse': nurse,
        'clients': clients,
        "lobby":lobby
    }

    return render(request,'nurse/nurse.html', context)

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def lobby_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    nurse = request.user.nurse
    lobby = nurse.lobby
    clients = lobby.clients.all()

    if request.method == 'POST' and 'preformed' in request.POST:
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.performed = True
        appointment.save()
        lobby.clients.remove(appointment)
        
        AnalysisRequest.objects.create(nurse=nurse, appointment=appointment)
        
        return redirect('lobby_detail', appointment_id=appointment.id)

    context = {
        'appointment': appointment
    }
    
    return render(request,'nurse/lobby/lobby_detail.html', context)

################################################################

# Analysis Requests

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_list(request):
    analysis_requests = AnalysisRequest.objects.select_related('appointment__client').all()
    context = {
        'analysis_requests': analysis_requests,
    }
    return render(request,'nurse/request/request_list.html', context)

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