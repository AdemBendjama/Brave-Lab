from django import forms

class ConfirmationForm(forms.Form):
    appointment_fee_paid = forms.BooleanField(required=True)
    
    def __init__(self, *args, **kwargs):
        appointment_fee = kwargs.pop('appointment_fee', None)
        super().__init__(*args, **kwargs)
        
        if appointment_fee:
            self.fields['appointment_fee_paid'].label = f'Appointment Fee Paid? (Appointment Fee: {appointment_fee})'
            