from django import forms
from .models import FinancialData

class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = ['csv_file']
