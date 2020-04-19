from django.urls import path
from .views import fundoo, Registrations, activate, Login, Forgotpassword, resetpassword, newpassword, image_upload
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [

    path('api-token-auth/', obtain_jwt_token), 
    path('api/token/', obtain_jwt_token),

    path('', fundoo, name = 'base'),
    path('registration/', Registrations.as_view(),  name = 'registration'),
    path('activate/<slug:surl>/',activate, name='activate'),
    path('login/',Login.as_view(), name = 'login'),

    path('forgotpassword/', Forgotpassword.as_view(), name = 'forgotpassword'),
    path('resetpassword/<slug:surl>', resetpassword, name='resetpassword'),
    path('newpassword/<user_reset>', newpassword.as_view(), name='newpassword'),
    path('upload/', image_upload, name = 'image_upload')
]