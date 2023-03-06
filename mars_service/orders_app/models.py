from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

from django.utils.translation import gettext_lazy


class Device(models.Model):
    """Device"""

    manufacturer = models.TextField(verbose_name="Производитель")
    model = models.TextField(verbose_name="Модель")

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        db_table = "devices"
        verbose_name = "Доступное оборудование"
        verbose_name_plural = "Доступное оборудование"


class Customer(models.Model):
    """Equipment end user"""

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_address = models.TextField(verbose_name="Адрес")
    customer_city = models.TextField(verbose_name="Город")

    def __str__(self):
        return self.customer_name

    class Meta:
        db_table = "customers"
        verbose_name = "Описание контрагента"
        verbose_name_plural = "Описание контрагентов"


class DeviceInField(models.Model):
    """Device in field"""

    serial_number = models.TextField(verbose_name="Серийный номер")
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Идентификатор пользователя")
    analyzer_id = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Идентификатор оборудования")
    owner_status = models.TextField(verbose_name="Статус принадлежности")

    def __str__(self):
        return f"{self.serial_number} {self.analyzer_id}"

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Описание контрагента"
        verbose_name_plural = "Описание контрагентов"


def status_validator(order_status):
    if order_status not in ["open", "closed", "in progress", "need info"]:
        raise ValidationError(
            gettext_lazy('%(order status)s is wrong order status'),
            params={'order_status': order_status},
        )


class Order(models.Model):
    """Order description class"""

    device = models.ForeignKey(DeviceInField, on_delete=models.RESTRICT, verbose_name="Оборудование")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Конечный пользователь")
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    last_updated_dt = models.DateTimeField(null=True, blank=True, verbose_name="Последнее изменение")
    order_status = models.TextField(validators=[status_validator], verbose_name="Статус заявки")

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

