from django.urls import path
from . import views

app_name = 'useraccountmanagement'

urlpatterns = [
    path('login/', views.login)
]
