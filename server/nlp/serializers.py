from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.Serializer):
    full_name=serializers.CharField(max_length=200)
    faculty=serializers.CharField(max_length=200)
    direction=serializers.CharField(max_length=200)
    profile=serializers.CharField(max_length=200)
    topic=serializers.CharField(max_length=200)
    keywords=serializers.ListField(child=serializers.CharField(max_length=200))
    
    class Meta:
        model=Student
        fields = ['full_name', 'faculty', 'direction', 'profile', 'topic', 'keywords']
        
    def create(self, validated_data):
        return Student.objects.create(**validated_data)