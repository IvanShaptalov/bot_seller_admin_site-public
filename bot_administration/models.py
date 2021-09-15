from django.db import models


class FuelType(models.Model):
    fuel_type_id = models.AutoField(unique=True, primary_key=True, serialize=True)
    fuel_type = models.CharField(max_length=50, verbose_name='Тип топлива')

    class Meta:
        verbose_name = 'Топливо'
        verbose_name_plural = 'Виды топлива'

    def __str__(self):
        return "{}".format(self.fuel_type)


class Fuel(models.Model):
    fuel_id = models.AutoField(unique=True, primary_key=True, serialize=True)
    fuel_count = models.IntegerField(verbose_name='Количество топлива, л')
    fuel_price = models.DecimalField(decimal_places=2, max_digits=29, verbose_name='Цена топлива', default=0)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.PROTECT, verbose_name='Тип топлива')

    class Meta:
        verbose_name = 'Топливо'
        verbose_name_plural = 'Топливо'

    def __str__(self):
        return "{} {} л. цена - {}".format(self.fuel_type,
                                           self.fuel_count,
                                           self.fuel_price)


class SignStatus(models.Model):
    status_id = models.AutoField(unique=True, primary_key=True, serialize=True)
    status = models.CharField(max_length=100, verbose_name='статус заявки')

    class Meta:
        verbose_name = 'Статус Заявки'
        verbose_name_plural = 'Статусы Заявок'

    def __str__(self):
        return "{} ".format(self.status)


class ClientSign(models.Model):
    sign_id = models.AutoField(unique=True, primary_key=True)
    first_last_name = models.CharField(max_length=100, verbose_name='ФИО')
    sign_code = models.IntegerField(default=0, unique=True, auto_created=True, verbose_name='Код заявки')
    source_type = models.CharField(max_length=10, verbose_name='Источник заявки')
    client_id = models.CharField(max_length=50, verbose_name='Айди клиента(в боте)')
    fuel = models.ForeignKey(Fuel, on_delete=models.PROTECT, verbose_name='Топливо')
    sign_date = models.DateTimeField(verbose_name='Дата заявки')
    sign_status = models.ForeignKey(SignStatus, on_delete=models.PROTECT, verbose_name='Статус заявки')
    client_phone_number = models.IntegerField(default=0, verbose_name='Номер телефона клиента')
    screenshot_link = models.CharField(max_length=100, verbose_name='Скриншот оплаты')

    class Meta:
        verbose_name = 'Заявка клиента'
        verbose_name_plural = 'Заявки клиентов'

    def __str__(self):
        return "Заявка №{} {} {}".format(self.sign_id,
                                         self.first_last_name,

                                         self.sign_status)

    @classmethod
    def create(cls, first_last_name):
        client_sign = cls(first_last_name=first_last_name)

        return client_sign