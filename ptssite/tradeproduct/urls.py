from django.urls import path
from .views import farmerActivity
from .views.farmerActivity import submitProduct, updateProducts, submit_details, delete_submittedProduct, change_details

from .views.buyerActivity import browseProduct, selectProduct, selectDriver

app_name = 'tradeproduct'

urlpatterns = [
    path('submitProduct/', submitProduct, name = 'submit'),
    path('updateSubmittedProduct/', updateProducts, name = 'update'),
    path('submit_details/<int:prodsub_id>/', submit_details, name = 'details'),
    path('delete_submittedProduct/<int:delete_id>/', delete_submittedProduct, name = 'delete'),
    path('change_details/<int:change_id>/', change_details, name = 'change'),

    path('browseProduct/', browseProduct, name = 'browse'),
    path('selectProduct/<int:select_id>/', selectProduct, name = 'select'),
    path('selectDriver/<str:chosenID_cap>/', selectDriver, name = 'selectDriver'),
]
