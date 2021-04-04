from django.urls import path
from . import views


urlpatterns = [
    path('gqw/',views.process_gqw,name='process_gqw'),
]
