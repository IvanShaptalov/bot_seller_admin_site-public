from rest_framework import serializers

from bot_administration.models import FuelType, Fuel, ClientSign


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = ('fuel_id', 'fuel_count', 'fuel_price', 'fuel_type')
        depth = 1


class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = ('fuel_type_id', 'fuel_type')


class ClientSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientSign
        fields = ('first_last_name', 'sign_code',
                  'source_type', 'client_id', 'fuel',
                  'sign_date', 'sign_status',
                  'client_phone_number', 'screenshot_link')
        depth = 2
