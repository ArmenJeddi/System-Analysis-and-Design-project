from django.urls import path

from . import views

app_name = 'finance'

urlpatterns = [
    path('depositmoney/', views.depositmoney, name = 'deposit'),
]
