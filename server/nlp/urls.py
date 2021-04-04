from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.model_form_upload, name='upload'),

]
