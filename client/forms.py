from django import forms 

TOPIC_CHOICES = [ ('Billing', 'Billing'),    ('Customer Service', 'Customer Service'),    ('Facilities', 'Facilities'),    ('Quality of Service', 'Quality of Service'),    ('Other', 'Other'),]

class ComplaintForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, required=True)
    description = forms.CharField(widget=forms.Textarea(),required=True)
                                  
                                  
class ClientContactForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)