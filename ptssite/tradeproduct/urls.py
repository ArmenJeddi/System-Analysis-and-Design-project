from django.urls import path
from .views import farmerActivity
from .views.farmerActivity import submitProduct, updateProducts, submit_details, delete_submittedProduct, change_details

from .views.buyerActivity import browseProduct, selectProduct, selectDriver, driver_details, confirmIt, order_detail_buyer

app_name = 'tradeproduct'

urlpatterns = [
    path('submitProduct/', submitProduct, name = 'submit'),
    path('updateSubmittedProduct/', updateProducts, name = 'update'),
    path('submit_details/<int:prodsub_id>/', submit_details, name = 'details'),
    path('delete_submittedProduct/<int:delete_id>/', delete_submittedProduct, name = 'delete'),
    path('change_details/<int:change_id>/', change_details, name = 'change'),

    path('browseProduct/', browseProduct, name = 'browse'),
    path('selectProduct/<int:select_id>/', selectProduct, name = 'select'),
    path('selectDriver/', selectDriver, name = 'selectDriver'),
    path('driver_details/<str:username>/', driver_details, name = 'driver_details'),
    path('confirmIt/<str:username>/', confirmIt, name = 'confirmation'),
    path('order_detail_buyer/<int:order_id>/', order_detail_buyer, name = 'order_detail_buyer'),


]
