from django.urls import path
from .views.Comments import commentOnFarmer, commentOnDriver

app_name = 'support'

urlpatterns = [
    path('commentOnFarmer/<int:order_id>/', commentOnFarmer, name = 'commentOnFarmer'),
    path('commentOnDriver/<int:order_id>/', commentOnDriver, name = 'commentOnDriver'),
]
