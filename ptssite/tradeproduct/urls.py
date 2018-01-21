from django.urls import path
from . import views

app_name = 'tradeproduct'

urlpatterns = [
    path('submitProduct/', views.submitProduct)
]
