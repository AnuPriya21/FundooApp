from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Registration, Note, Label

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        
class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model =User
        fields = ['email']

class ResetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password']
    
class NoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Note
        fields = ['id','title','text','archive','trash']

class DisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['id']

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['label']

class RestoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['trash']

