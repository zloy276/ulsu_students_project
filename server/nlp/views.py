from django.shortcuts import render
from .forms import UploadForm

from .models import Student

def upload(request):
    
    return render(request,'upload.html',{'form':UploadForm()})

def show(request):
    
    request.FILES['file']
    
    