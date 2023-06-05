from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required , permission_required
from auditor.forms import NurseForm, UpdateTestsForm
from auditor.models import Auditor
from django.contrib.auth.models import User

from main_home.models import AnalysisRequest, ChatRoom, Component, Invoice, Laboratory, Message, Report, Test, TestResult


from django.core.serializers import serialize
from django.utils import formats

from nurse.models import Nurse
# Create your views here.

################################################################

# Home - Stats

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def auditor_home(request):
    
    
    return render(request,'auditor/auditor.html')

################################################################

# Chat

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    
    context = {
        'chat_rooms': chat_rooms
    }
    
    return render(request,'auditor/message/chat_rooms.html', context)

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def message_chat(request,room_id):
    room = ChatRoom.objects.get(id=room_id)
    
    messages = Message.objects.filter(room=room)
    messages = messages.order_by('timestamp')
    
    context={
        'room_id':room_id,
        'room':room,
        'messages':messages,
    }
    
    return render(request,'auditor/message/message_chat.html',context)


@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def auditor_send(request):
    room_id = request.POST.get('room_id')
    room = ChatRoom.objects.get(id=room_id)
    message = request.POST.get('message')
    
    sender = request.user  # Current auditor
    receiver = room.nurse.user # the nurse from the room
    
    # Create and save the message with the sender, receiver, and other fields
    message = Message.objects.create(sender=sender, receiver=receiver, room_id=room_id, content=message)
    
    return HttpResponse('Message sent successfully')

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def getMessages(request):
    room_id = request.GET.get('room_id')
    room = ChatRoom.objects.get(id=room_id)
    nurse = room.nurse
    messages = Message.objects.filter(sender=nurse.user) | Message.objects.filter(receiver=nurse.user)
    messages = messages.order_by('timestamp')
    auditor_id = request.user.id    

    def serialize_timestamp(timestamp):
        return formats.date_format(timestamp, "F j, Y, P")

    serialized_messages = []
    for message in messages:
        serialized_message = {
            'id': message.id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'room_id': message.room_id,
            'content': message.content,
            'timestamp': serialize_timestamp(message.timestamp),
        }
        serialized_messages.append(serialized_message)
        
    return JsonResponse({"messages":serialized_messages,"auditor_id":auditor_id})


################################################################

# Analysis Requests

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
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
    return render(request,'auditor/request/request_list.html', context)

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def request_detail(request, analysis_request_id):
    analysis_request = get_object_or_404(AnalysisRequest, id=analysis_request_id)
    form = NurseForm()
    context = {
        'analysis_request': analysis_request,
        "form":form,
    }
    
    return render(request,'auditor/request/request_detail.html', context)


@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def change_nurse(request, analysis_request_id):
    
    if request.method == "POST":
        
        form = NurseForm(request.POST)
        
        if form.is_valid():
            nurse = form.cleaned_data['nurse']
            user = User.objects.get(username=nurse)
            nurse = Nurse.objects.get(user = user)
            analysis_request = AnalysisRequest.objects.get(id = analysis_request_id)
            analysis_request.nurse = nurse
            analysis_request.save()
            
            # nurse = Nurse.objects.get(id=nurse_id)
            print(analysis_request.nurse)
    
    
    return redirect('auditor_request_detail',analysis_request_id=analysis_request_id)


################################################################

# Results

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def result_list(request):
    unapproved_results = TestResult.objects.filter(approved=False)
    approved_results = TestResult.objects.filter(approved=True)
    
    context = {
        'unapproved_results': unapproved_results,
        'approved_results': approved_results,
    }
    return render(request,'auditor/result/result_list.html', context)

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def result_detail(request , test_result_id):
    test_result = get_object_or_404(TestResult, id=test_result_id)
  
    context = {
        'test_result': test_result,
    }

    return render(request,'auditor/result/result_detail.html', context)


@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def approve_result(request, test_result_id):
    
    if 'approve' in request.POST:
        test_result = get_object_or_404(TestResult, id=test_result_id)

        # Update the approval status of the test result
        test_result.approved = True
        test_result.save()
        
        description = request.POST.get("report-desc")
        report = Report.objects.create(test_result=test_result,description=description)
        laboratory = Laboratory.objects.get(name="Brave Laboratory")
        
        invoice = Invoice.objects.create(
            report=report,
            total_price=report.test_result.request.appointment.total_price,
            payment_status=report.test_result.request.appointment.payment_status,
            client=report.test_result.request.appointment.client,
            laboratory=laboratory
        )
        

    return redirect('test_result_detail', test_result_id=test_result_id)

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def result_update(request, test_result_id):
    test_result = get_object_or_404(TestResult, id=test_result_id)

    if request.method == 'POST':
        # Process the form submission to update the tests

        form = UpdateTestsForm(request.POST, test_result=test_result)
        if form.is_valid():
            # Iterate over the tests in the form data and update their values
            for test in test_result.request.tests.all():
                test_value_key = f'test_{test.id}_value'
                if test_value_key in form.cleaned_data:
                    test.value = form.cleaned_data[test_value_key]
                    test.save()

                    # Iterate over the components of the test and update their values
                    for component in test.components.all():
                        component_value_key = f'component_{component.id}_value'
                        if component_value_key in form.cleaned_data:
                            component.value = form.cleaned_data[component_value_key]
                            component.save()

            return redirect('test_result_detail', test_result_id=test_result_id)
    else:
        # Display the form for modifying tests

        form = UpdateTestsForm(test_result=test_result)

    context = {
        'test_result': test_result,
        'form': form,
    }

    return render(request, 'auditor/result/result_update.html', context)

################################################################

# Reports

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def report_list(request):
    reports = Report.objects.all()

    context = {
        'reports': reports,
    }
    return render(request,'auditor/report/report_list.html', context)

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    context = {
        'report': report,
    }
    return render(request,'auditor/report/report_detail.html', context)
