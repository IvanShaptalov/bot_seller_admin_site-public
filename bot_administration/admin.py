import json

import requests
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin

import botseller_django_administration.settings
from bot_administration.models import FuelType, ClientSign, SignStatus, Fuel

from botseller_django_administration import settings


# solved find way to send talons
# todo create tests
def accept_sign(model_admin, request, queryset):
    for obj in queryset:
        if isinstance(obj, ClientSign):
            # send bot to telegram
            if obj.sign_status.status != 'Одобрено':
                if obj.source_type == 'telegram':
                    # form info to bot
                    text = 'Заказ#{}\n{} {} {}\nПодтвержден'.format(obj.sign_code or "",
                                                                    obj.fuel.fuel_type.fuel_type or "",
                                                                    obj.fuel.fuel_count,
                                                                    "Цена: {}".format(obj.fuel.fuel_price or ""))
                    token_count = int(int(obj.fuel.fuel_count) / 10)
                    # todo add token to path
                    url = '{}/add'.format(settings.TELEGRAM_ADDRESS)
                    print(url)
                    data = {
                        "client_id": obj.client_id,
                        "text": text,
                        "token_count": token_count,
                        # todonow check this moment
                        "fuel_type": obj.fuel.fuel_type.fuel_type
                    }
                    data_json = json.dumps(data)
                    result = " "
                    try:
                        result = requests.post(url, json=data_json)
                    except Exception as e:
                        print(e)
                        print('error with bot connection')
                        ModelAdmin.message_user(level=messages.WARNING, message="Телеграм бот не активирован!",
                                                request=request,
                                                self=obj)
                        return
                    if result.text == 'tokens_send':
                        obj.sign_status = SignStatus.objects.filter(status='Одобрено').first()
                        obj.check()
                        obj.save()
                        ModelAdmin.message_user(level=messages.SUCCESS, message="Статут заказа изменен!{}".format("заявка№ {}".format(obj.sign_code)),
                                                request=request,
                                                self=obj)
                    else:
                        pattern = "заявка№ {}".format(obj.sign_code)
                        message = "Токены типа {} отсутствуют!{}".format(
                            obj.fuel.fuel_type.fuel_type, pattern) or "Токены данного типа отсутствуют {}".format(pattern)
                        ModelAdmin.message_user(level=messages.WARNING, message=message,
                                                request=request,
                                                self=obj)
            else:
                ModelAdmin.message_user(level=messages.WARNING, message="Статус заявки {} уже одобрен".format(obj.sign_code),
                                        request=request,
                                        self=obj)


def decline_sign(model_admin, request, queryset):
    for obj in queryset:
        if isinstance(obj, ClientSign):
            if obj.sign_status.status != 'Отклонено':
                if obj.source_type == 'telegram':
                    url = '{}/decline'.format(settings.TELEGRAM_ADDRESS)
                    message = {'chat_id': obj.client_id,
                               'text': 'Заказ#{}\n{} {} {}\nОтклонен'.format(obj.sign_code or "",
                                                                             obj.fuel.fuel_type.fuel_type or "",
                                                                             obj.fuel.fuel_count,
                                                                             "Цена: {}".format(
                                                                                 obj.fuel.fuel_price or ""))}
                    try:
                        # decline
                        result = requests.post(url, data=json.dumps(message))
                        print(result.text)
                    except Exception as e:
                        print(e, type(e))
                        ModelAdmin.message_user(level=messages.WARNING, message="Телеграм бот не активирован!",
                                                request=request,
                                                self=obj)
                        return
                    if result and result.text == '200':
                        obj.sign_status = SignStatus.objects.filter(status='Отклонено').first()
                        obj.check()
                        obj.save()
                        ModelAdmin.message_user(level=messages.SUCCESS, message="Статут заказа изменен!{}".format("заявка№ {}".format(obj.sign_code)),
                                                request=request,
                                                self=obj)
            else:
                ModelAdmin.message_user(level=messages.WARNING, message="Статус заявки уже отклонен {}".format("заявка№ {}".format(obj.sign_code)),
                                        request=request,
                                        self=obj)


accept_sign.short_description = "Подтвердить заявку"
decline_sign.short_description = "Отклонить заявку"


class AdminFuelType(admin.ModelAdmin):
    list_display = ('fuel_type',)
    fields = ('fuel_type',)


class AdminClientSign(admin.ModelAdmin):
    list_display = (
        'first_last_name', 'sign_code', 'source_type', 'client_id', 'fuel',
        'sign_date',
        'sign_status',
        'client_phone_number',
        'screenshot_link')
    fields = (
        'sign_code',
        'fuel',
        ('client_phone_number', 'first_last_name'),
        'client_id', 'source_type',
        'screenshot_link',
        'sign_date',)
    list_filter = ('sign_status',)
    ordering = ('-sign_date',)
    actions = [accept_sign, decline_sign]


class AdminFuel(admin.ModelAdmin):
    list_display = ('fuel_count', 'fuel_price', 'fuel_type')
    fields = ('fuel_count', 'fuel_price', 'fuel_type')


class AdminSignStatus(admin.ModelAdmin):
    list_display = ('status',)
    fields = ('status',)


admin.site.register(FuelType, AdminFuelType)
admin.site.register(ClientSign, AdminClientSign)
admin.site.register(SignStatus, AdminSignStatus)
admin.site.register(Fuel, AdminFuel)
