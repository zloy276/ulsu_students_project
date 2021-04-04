from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Student

# Create your views here.
@api_view(['POST'])
def process_gqw(request,format='json'):
    return Response({},status=200)