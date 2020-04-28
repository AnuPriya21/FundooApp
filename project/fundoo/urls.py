from django.urls import path
from .views import home, fundoo, Registrations, activate, Login, logout,Forgotpassword, resetpassword, newpassword, image_upload, Createnote, Updatenote, Createlabel, Updatelabel
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [

    path('api-token-auth/', obtain_jwt_token), 
    path('api/token/', obtain_jwt_token),

    path('fundoo/', fundoo, name='fundoo'),
    path('', home, name = 'home'),
    path('registration/', Registrations.as_view(),  name = 'registration'),
    path('activate/<slug:surl>/',activate, name='activate'),
    path('login/',Login.as_view(), name = 'login'),
    path('logout/', logout, name = 'logout'),

    path('forgotpassword/', Forgotpassword.as_view(), name = 'forgotpassword'),
    path('resetpassword/<slug:surl>', resetpassword, name='resetpassword'),
    path('newpassword/<user_reset>', newpassword.as_view(), name='newpassword'),
    path('upload/', image_upload, name = 'image_upload'),

    path('createnote/', Createnote.as_view(), name = 'createnote'),
    path('updatenote/<int:id>', Updatenote.as_view(), name = 'updatenote'),
    path('createlabel/', Createlabel.as_view(), name = 'createlabel'),
    path('updatelabel/<int:id>', Updatelabel.as_view() ,name="labelupdate"),

] 