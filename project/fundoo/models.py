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

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    text = models.TextField()
    archive = models.BooleanField(default=False)
    trash = models.BooleanField(default=False)
    note_label = models.ManyToManyField('Label', blank=True)


    def __str__(self):
        return str(self.title)
        
class Label(models.Model):
    user = models.ForeignKey(User, related_name='Label', on_delete=models.CASCADE)
    label = models.CharField(max_length=50, blank=True)

    def __str__(self):  
        return str(self.label)