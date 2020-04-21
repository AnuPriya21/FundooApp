from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Registration, Profile

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
    

class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']