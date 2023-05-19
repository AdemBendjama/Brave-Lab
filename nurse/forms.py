# forms.py
from django import forms
from main_home.models import TestOffered

class AddTestForm(forms.Form):
    test_offered = forms.ModelChoiceField(queryset=TestOffered.objects.none(), empty_label=None)

    def __init__(self, appointment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing_tests = appointment.tests_requested.all()
        self.fields['test_offered'].queryset = TestOffered.objects.exclude(id__in=existing_tests.values_list('id', flat=True))