from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime


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
        return f"{self.customer_name} по адресу {self.customer_address}"

    class Meta:
        db_table = "customers"
        verbose_name = "Описание контрагента"
        verbose_name_plural = "Описание контрагентов"


class DeviceInField(models.Model):
    """Device in field"""

    serial_number = models.TextField(verbose_name="Серийный номер")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Идентификатор пользователя")
    analyzer = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Идентификатор оборудования")
    owner_status = models.TextField(verbose_name="Статус принадлежности")

    def __str__(self):
        return f"{self.analyzer} с\н {self.serial_number} в {self.customer}"

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Оборудование в полях"
        verbose_name_plural = "Оборудование в полях"


class Order(models.Model):
    """Order description class"""

    statuses = (("open", "открыта"),
                ("closed", "закрыта"),
                ("in progress", "в работе"),
                ("need info", "требует уточнений"),)

    device = models.ForeignKey(DeviceInField, on_delete=models.RESTRICT, verbose_name="Оборудование")
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    last_updated_dt = models.DateTimeField(null=True, blank=True, verbose_name="Последнее изменение")
    order_status = models.TextField(verbose_name="Статус заявки", choices=statuses)

    def __str__(self):
        return f"Заявка №{self.pk} для {self.device}"

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

