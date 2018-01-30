from django.urls import path
from .views import *

app_name = 'useraccountmanagement'

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('registration/', RegistrationView.as_view()),
    path('registration/driver/', DriverRegistrationView.as_view()),
    path('registration/customer/', CustomerRegistrationView.as_view()),
    path('registrationsuccess/', RegistrationSuccessView.as_view()),
    path('passwordrecovery/', PasswordRecoveryView.as_view()),
    path('passwordrecoverysuccess/', PasswordRecoverySuccessView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('updateprofile/<str:username>/', UpdateProfileView.as_view()),
    path('updateprofilesuccess/', UpdateProfileSuccessView.as_view()),
    path('logout/', LogoutView.as_view())
]
