from django.urls import path
from .views import farmerActivity
from .views.farmerActivity import submitProduct, removeProduct, submit_details

app_name = 'tradeproduct'

urlpatterns = [
    path('submitProduct/', submitProduct),
    path('updateSubmittedProduct/', removeProduct),
    path('submit_details/<int:prodsub_id>/', submit_details, name = 'submit_details')
]
