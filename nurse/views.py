from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required , permission_required
from main_home.models import AnalysisRequest, Appointment, Lobby
from django.utils import timezone

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
    pending_requests = analysis_requests.filter(status=AnalysisRequest.PENDING)
    working_on_requests = analysis_requests.filter(status=AnalysisRequest.WORKING_ON)
    finished_requests = analysis_requests.filter(status=AnalysisRequest.FINISHED)
    
    context = {
        'pending_requests': pending_requests,
        'working_on_requests': working_on_requests,
        'finished_requests': finished_requests,
    }
    return render(request,'nurse/request/request_list.html', context)

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_detail(request, analysis_request_id):
    analysis_request = get_object_or_404(AnalysisRequest, id=analysis_request_id)
    context = {
        'analysis_request': analysis_request,
    }
    return render(request,'nurse/request/request_detail.html', context)


@login_required
@permission_required('nurse.change_analysisrequest', raise_exception=True)
def start_analysis(request, analysis_request_id):
    analysis_request = get_object_or_404(AnalysisRequest, id=analysis_request_id)

    if request.method == 'POST':
        analysis_request.start_time = timezone.now()
        analysis_request.status = AnalysisRequest.WORKING_ON
        analysis_request.accepted = True
        analysis_request.save()

        return redirect('request_detail', analysis_request_id=analysis_request.id)

    return redirect('request_list')


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