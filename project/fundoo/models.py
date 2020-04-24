from django.db import models
from django import forms
from django.contrib.auth.models import User


class Registration(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField(max_length = 100)
    password1 = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.id

class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return self.file

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=200)
    
    def __str__(Self):
        return self.title
