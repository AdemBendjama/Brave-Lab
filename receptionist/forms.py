from django import forms

class ConfirmationForm(forms.Form):
    appointment_fee_paid = forms.BooleanField(required=True)
    tests_fee_paid = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        tests_fee = kwargs.pop('tests_fee', None)
        appointment_fee = kwargs.pop('appointment_fee', None)
        super().__init__(*args, **kwargs)
        
        if appointment_fee:
            self.fields['appointment_fee_paid'].label = f'Appointment Fee Paid? (Appointment Fee: {appointment_fee})'
            
        if tests_fee:
            self.fields['tests_fee_paid'].label = f'Tests Paid (Total Price: {tests_fee})'
