from django import form

class UploadForm(form.Form):
    file=form.FileField()
    