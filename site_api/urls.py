from django.urls import path

from site_api.views import get_all_fuel_pricelist, get_new_sign

app_name = 'api'

urlpatterns = [
    path('get_fuel/<str:api_key>', get_all_fuel_pricelist, name='get_fuel'),
    path('get_new_sign/<str:api_key>', get_new_sign, name='get_new_sign'),
]
