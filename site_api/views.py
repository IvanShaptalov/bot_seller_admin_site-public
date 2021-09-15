import json

from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
import botseller_django_administration.settings
from bot_administration.models import ClientSign, Fuel, FuelType
from site_api import utils
from site_api.serializers import FuelSerializer, FuelTypeSerializer, ClientSignSerializer
from django.views.defaults import permission_denied


@api_view(['GET'])
def get_all_fuel_pricelist(request, api_key):
    if api_key == botseller_django_administration.settings.SECRET_TOKEN:
        price_list = Fuel.objects.all()
        serializer = FuelSerializer(price_list, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    else:
        raise PermissionDenied()


@api_view(['POST'])
def get_new_sign(request, api_key):
    if api_key == botseller_django_administration.settings.SECRET_TOKEN:
        if request.method == 'POST':
            sign = utils.create_sign(request.data)
            if sign:
                # print(request.data)
                sign.save()
                return Response('sign added!', status=HTTP_201_CREATED)
            else:
                return Response('bad request, unique constraint failed', status=HTTP_400_BAD_REQUEST)
    return PermissionDenied()
