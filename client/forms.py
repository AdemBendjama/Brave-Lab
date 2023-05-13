from django import forms 

class ClientContactForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)