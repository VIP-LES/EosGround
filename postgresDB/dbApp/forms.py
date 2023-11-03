from django import forms

class TerminalInputForm(forms.Form):
    command = forms.CharField(max_length=255)
