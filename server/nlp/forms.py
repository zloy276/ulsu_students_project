from django import forms
from .models import UploadedFile


class DocumentForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('description', 'document',)
