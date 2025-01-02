# transactions/forms.py
from django import forms
from .models import *
class UploadFileForm(forms.Form):
    file = forms.FileField()

class BankStatementSelectionForm(forms.Form):
    bank = forms.ModelChoiceField(queryset=Bank.objects.all(), label="Select Bank")
    statement_type = forms.ModelChoiceField(queryset=StatementType.objects.all(), label="Select Statement Type")

    