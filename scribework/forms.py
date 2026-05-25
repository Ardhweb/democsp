from django import forms
from django.core.validators import FileExtensionValidator

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        validators=[FileExtensionValidator(['xls', 'xlsx'])],
        label="Select an Excel file"
    )