from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializer import RegistrationSerializer, LoginSerializer, ResetPasswordSerializer, NoteSerializer
from django.contrib.auth.models import User, auth 
from django.http import HttpResponse, response
from .token import token_activation
from django.contrib.sites.shortcuts import get_current_site
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from django.template.loader import render_to_string
from django.core.mail import send_mail
from project.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from project.settings import SECRET_KEY
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.validators import validate_email
import jwt
from django.core.cache import cache
from project import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Upload, Note


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def home(request):
    return render(request, 'base.html')

def fundoo(request):
    context = {}
    context['user'] = request.user
    return render(request, 'fundoo.html')
 
class Registrations(GenericAPIView):

    serializer_class = RegistrationSerializer

    def get(self,request):
        return render(request, 'registration.html')

    def post(self,request):

        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 =  request.POST.get('password1')

        if password == password1:
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
            print('user created')
            token = token_activation(username, password)
            current_site = get_current_site(request)
            domain = current_site.domain
            url = str(token)
            surl = get_surl(url)
            z = surl.split("/")
            mail_subject = "Click the link below to activate your account"
            message = render_to_string('emailverification.html', {
                'user' : User.username,
                'doamin' : domain,
                'surl' : z[2]
            })
            print(message)
            rep = email
            email = EmailMessage(mail_subject, message, to=[rep])
            email.send()
            return HttpResponse('confirmation mail sent!!! Please confirm your email address to complete the registration')
            messages.success(request, 'Your Account has been successfully Activated!!!')

        else:
            messages.error(request, 'Invalid Username or Password')
            print("Password didn match")
            return redirect("/registration/")

def activate(request,surl):
    print("Activate url is ", surl)   
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, "your account is active now")
            return redirect("/")      
        else:           
            messages.info(request, 'was not able to sent the email')          
            return redirect("/registration/")
    
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect("/registration/")

class Login(GenericAPIView):
    
    serializer_class = LoginSerializer

    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        data =request.data 
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(username=username, password=password)
        token = token_activation(username, password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                print("Sucessfully Loged in")
                cache.set(user.username,token)
                print(cache.get(user.username,token))
                return Response({'message':'token sent',"token":token}) 
                #return redirect("/fundoo/")
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Invalid Credentials")
        return redirect("/")
    
def logout(request):
    auth.logout(request)
    return redirect("/login/")

class Forgotpassword(GenericAPIView):

    serializer_class = ResetPasswordSerializer

    def get(self,request):
        return render(request, 'forgot_password.html')

    def post(self,request):
        email = request.data['email']
        validate_email(email)

        try:
            user = User.objects.filter(email = email)
            useremail = user.values()[0]['email']
            username = user.values()[0]['username']
            id = user.values()[0]['id'] 

            print('useremail', useremail)
            if user is not None:
                
                token = token_activation(username, id)
                url = str(token)
                surl = get_surl(url)
                slug_url = surl.split('/')

                mail_subject = "Click the link below to reset your account password"
                mail_message = render_to_string('resetpassword.html', {
                    'user': username,
                    'domain': get_current_site(request).domain,
                    'surl': slug_url[2]
                })
                print('mail message',mail_message)

                recipientemail = useremail
                email = EmailMessage(mail_subject, mail_message, to=[recipientemail])
                email.send()
                return HttpResponse('confirmation mail sent!!!Click on the link to change password')
       
        except TypeError:
            print("User dosent exist")
        return HttpResponse("Enter correct email id")

def resetpassword(request, surl):
    
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        if user is not None:
            return redirect('/newpassword/' + str(user))
        else:
            return redirect('/forgot_password/')
    except KeyError:
        return HttpResponse("Key Error")

class newpassword(GenericAPIView):

    serializer_class = ResetPasswordSerializer
    
    def get(self,request,user_reset):
        return render(request,'newpassword.html')
    
    def post(self,request,user_reset):
        data=request.data 

        password = data.get('password')
        try:
            user = User.objects.get(username=user_reset)
            user.set_password(password)
            user.save()
            messages.info(request, 'Password Updated Successfully')
            return redirect('/login/')
        except KeyError:
            return HttpResponse("Key Error")


def image_upload(request):

    if request.method == 'POST':

        image_file = request.FILES['image_file']
        upload = Upload(file=image_file)
        upload.save()
        image_url = upload.file.url

        return render(request, 'upload.html', {
            'image_url': image_url
        })

    return render(request, 'upload.html')

class Createnote(GenericAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get(self, request):
        user = request.user.id
        notes = Note.objects.filter(archive=False,trash=False)
        print(notes)
        return Response(notes.values())

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        print(request.data['title'])

        if serializer.is_valid():
            print("valid")
            user = request.user.id
            print(user)
            serializer.save(user_id=user)
            return Response('note is saved')
        return Response("Enter some notes")

