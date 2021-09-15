import datetime
import json

from bot_administration.models import ClientSign, Fuel, SignStatus

fuel_param_list = [
    'fuel_id', 'first_last_name',
    'source_type', 'sign_code',
    'client_id', 'sign_date',
    'client_phone_number',
    'screenshot_link'
]


def data_validation(data):
    for param in fuel_param_list:
        try:
            res = data.get(param)
            if not res:
                raise KeyError()
        except Exception as key_error:
            print(key_error)
            break

    return True


def create_sign(data) -> ClientSign or None:
    print(data)
    res = dict(data)
    if data_validation(data):
        fuel = Fuel.objects.filter(fuel_id=int(res['fuel_id'][0]))
        sign_status = SignStatus.objects.filter(status_id=3)
        if fuel and sign_status and not ClientSign.objects.filter(sign_code=res['sign_code'][0]):
            sign = ClientSign.create(res['first_last_name'][0])
            sign.source_type = res['source_type'][0]
            sign.sign_code = res['sign_code'][0]
            sign.client_id = res['client_id'][0]
            sign.fuel = fuel.first()
            date_string = res['sign_date'][0]
            print(date_string)
            assert isinstance(date_string, str)
            sign.sign_date = date_string
            sign.sign_status = sign_status.first()
            sign.client_phone_number = res['client_phone_number'][0]
            sign.screenshot_link = res['screenshot_link'][0]
            sign.check()
            return sign
    return None
