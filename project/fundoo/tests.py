from django.urls import reverse
import unittest
import pytest
from django.http import HttpRequest
from rest_framework import status
from rest_framework.test import APITestCase
from project.settings import BASE_URL
from django.test import Client 
from .import views


client = Client()

@pytest.mark.django_db
class TestUrls(unittest.TestCase):

    def test_on_registration(self):
        
        url = BASE_URL + reverse("registration")
        Userdata = {'name': 'priya', 'username':'priya', 'email':'priya@gmail.com', 'password':'ab', 'password1':'ab'}
        response = client.post(path=url, data=Userdata, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_on_empty_parameters(self):
        
        url = BASE_URL + reverse("registration")
        Userdata = {'name': '', 'username':'', 'email':'', 'password':'', 'password1':''}
        response = client.post(path=url, data=Userdata, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        
        url = BASE_URL + reverse("login")
        Userdata = {'username':'arpi' , 'password':'123'}
        response = client.post(path=url, data=Userdata, format='json')
        self.assertEqual(response.status_code, 302)
    
    def test_login_empty_params(self):
        
        url = BASE_URL + reverse("login")
        Userdata = {'username':'' , 'password':''}
        response = client.post(path=url, data=Userdata, format='json')
        self.assertEqual(response.status_code, 302)
    
    def test_forgot_password(self):
        
        url = BASE_URL + reverse("forgotPassword")
        Userdata = {'email':'priya@gmail.com'}
        response = client.post(path=url, data=Userdata, format='json')
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_empty(self):
        
        url = BASE_URL + reverse("forgotPassword")
        Userdata = {'email':''}
        response = client.post(path=url, data=Userdata, format='json')
        self.assertEqual(response.status_code, 404)