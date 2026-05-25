from django.shortcuts import render

# Create your views here.
from .forms import ExcelUploadForm

def commission_data_ingestion(request):
	form = ExcelUploadForm()
	return render(request, 'scribework/data-ingestion.html', {'form':form,})