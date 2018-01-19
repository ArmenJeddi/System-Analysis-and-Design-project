from django.urls import path

from . import views

app_name = 'reporting'

urlpatterns = [
    path('listbuyers/', views.listbuyers),
    path('listdrivers/', views.listdrivers),
    path('listfarmers/', views.listfarmers),
    path('listorders/', views.listorders),
    path('listproducts/', views.listproducts),
    path('listpurchases/', views.listpurchases),
    path('listtransports/', views.listtransports)
]
