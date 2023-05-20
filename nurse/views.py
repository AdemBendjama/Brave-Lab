
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required , permission_required
from main_home.models import AnalysisRequest, Appointment, Lobby, Payment, Test , TestResult
from django.utils import timezone
from nurse.forms import AddComponentForm, AddTestForm, TestFinalizeForm

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
        
        analysis_request = AnalysisRequest.objects.create(nurse=nurse, appointment=appointment)
        
        # Get the tests_requested from the appointment and create Test objects for each one
        tests_requested = appointment.tests_requested.all()
        for test_offered in tests_requested:
            test = Test.objects.create(test_offered=test_offered)
            analysis_request.tests.add(test)
        
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
@permission_required('nurse.view_nurse', raise_exception=True)
def start_analysis(request, analysis_request_id):
    analysis_request = get_object_or_404(AnalysisRequest, id=analysis_request_id)

    if request.method == 'POST':
        analysis_request.start_time = timezone.now()
        analysis_request.status = AnalysisRequest.WORKING_ON
        analysis_request.accepted = True
        analysis_request.save()

        return redirect('request_detail', analysis_request_id=analysis_request.id)

    return redirect('request_list')

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def finish_analysis(request, analysis_request_id):
    analysis_request = get_object_or_404(AnalysisRequest, id=analysis_request_id)
    
    if request.method == 'POST':
        if analysis_request.all_tests_confirmed():
            # Mark analysis request as finished
            analysis_request.finished = True
            analysis_request.finish_time = timezone.now()
            analysis_request.status = AnalysisRequest.FINISHED
            analysis_request.save()
            
            # Create TestResult object
            test_result = TestResult.objects.create(
                request=analysis_request,
                duration=analysis_request.duration_unformated()
            )
            
            return redirect('request_detail', analysis_request.id)
    
    # If the request is not a POST request or tests are not confirmed, redirect back to request detail page
    return redirect('request_detail', analysis_request.id)


################################################################

# Analysis Requests Tests

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_add(request, analysis_request_id):
    
    analysis_request = AnalysisRequest.objects.get(id=analysis_request_id)
    appointment = analysis_request.appointment
    
    if request.method == 'POST':
        form = AddTestForm(appointment, request.POST)
        if form.is_valid():
            test_offered = form.cleaned_data['test_offered']
            test = Test.objects.create(test_offered=test_offered)
            analysis_request.tests.add(test)
            
            # Update payment status and fees
            payment = Payment.objects.get(appointment=analysis_request.appointment)
            payment.payed_nurse_tests_fee = False
            payment.nurse_tests_fee += test_offered.price
            payment.save()
            
            appointment.total_price += test_offered.price
            appointment.payment_status = False
            appointment.save()
            
            return redirect('request_test_list', analysis_request_id=analysis_request_id)
    else:
        form = AddTestForm(appointment)
        
    context = {
        'form': form, 
        'analysis_request': analysis_request
    }
        
    return render(request,'nurse/request/test/request_test_add.html', context)

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_add_component(request, analysis_request_id, test_id):
    analysis_request = AnalysisRequest.objects.get(id=analysis_request_id)
    test = Test.objects.get(id=test_id)

    if request.method == 'POST':
        form = AddComponentForm(request.POST, test=test)
        if form.is_valid():
            component = form.cleaned_data['component']
            test.components.create(info=component)
            return redirect('request_test_add_component', analysis_request_id=analysis_request_id, test_id=test_id)
    else:
        form = AddComponentForm(test=test)

    context = {
        'form': form,
        'analysis_request': analysis_request,
        'test': test
    }


    return render(request,'nurse/request/test/request_test_add_component.html', context)

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_list(request, analysis_request_id):
    analysis_request = get_object_or_404(AnalysisRequest, id=analysis_request_id)
    tests = analysis_request.tests.all()
    context = {
        'analysis_request': analysis_request,
        'tests': tests
    }
    
    return render(request,'nurse/request/test/request_test_list.html', context)

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_detail(request, analysis_request_id, test_id):
    analysis_request = AnalysisRequest.objects.get(id=analysis_request_id)
    test = Test.objects.get(id=test_id)

    context = {
        'analysis_request': analysis_request,
        'test': test
    }
    
    return render(request,'nurse/request/test/request_test_detail.html', context)

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def request_test_finalize(request, analysis_request_id, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.method == 'POST':
        form = TestFinalizeForm(request.POST, instance=test)
        if form.is_valid():
            form.save()  # Save the form data
            test.confirmed = True  # Mark the test as confirmed
            test.save()
            return redirect('request_test_detail', analysis_request_id=analysis_request_id, test_id=test_id)
    else:
        form = TestFinalizeForm(instance=test)

    context = {
        'form': form,
        'analysis_request_id': analysis_request_id,
        'test': test,
    }


    return render(request,'nurse/request/test/request_test_finalize.html', context)

################################################################

# Chat

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def message_chat(request):
    
    return render(request,'nurse/message/message_chat.html')


################################################################


# Result


@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def result_list(request):
    
    return render(request,'nurse/result/result_list.html')

@login_required
@permission_required('nurse.view_nurse', raise_exception=True)
def result_detail(request, result_id):
    
    return render(request,'nurse/result/result_detail.html')

