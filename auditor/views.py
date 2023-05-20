from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required , permission_required
from auditor.forms import UpdateTestsForm

from main_home.models import AnalysisRequest, Component, Invoice, Laboratory, Report, Test, TestResult
from auditor.forms import ReportForm

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
def message_chat(request):
    
    return render(request,'auditor/message/message_chat.html')

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

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def report_add(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save()
            laboratory = Laboratory.objects.get(name="Brave Laboratory")
            
            invoice = Invoice.objects.create(
                report=report,
                total_price=report.test_result.request.appointment.total_price,
                payment_status=report.test_result.request.appointment.payment_status,
                client=report.test_result.request.appointment.client,
                laboratory=laboratory
            )
            
            return redirect("report_list")
    else:
        form = ReportForm()

    context = {
        'form': form,
    }
    return render(request,'auditor/report/report_add.html', context)