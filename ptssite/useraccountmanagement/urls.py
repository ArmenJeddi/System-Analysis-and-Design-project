from django.urls import path
from . import views

app_name = 'useraccountmanagement'

urlpatterns = [
    path('login/', views.login),
    path('registration/', views.registration),
    path('registration/driver/', views.registration),
    path('registration/customer/', views.registration),
    path('passwordrecovery/', views.PasswordRecoveryView.as_view()),
    path('profile/', views.profile),
    path('updateprofile/', views.UpdateProfileView.as_view()),
    path('logout/', views.logout)
]
