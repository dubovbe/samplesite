from django.db import models
from django.contrib.postgres.fields import ArrayField


class Courier(models.Model):
    courier_id = models.IntegerField(verbose_name='Уникальный идентификатор')
    courier_type = models.CharField(max_length=50, verbose_name='Тип')
    regions = ArrayField(models.IntegerField(verbose_name='Список идентификаторов районов'))
    working_hours = ArrayField(models.CharField(max_length=50, verbose_name='График работы'))
    rating = models.FloatField(null=True, blank=True, verbose_name='Рейтинг')
    earnings = models.FloatField(null=True, blank=True, verbose_name='Заработок')

    class Meta:
        verbose_name_plural = 'Курьеры'
        verbose_name = 'Курьер'
        ordering = ['-rating']


class Order(models.Model):
    order_id = models.IntegerField(verbose_name='Уникальный идентификатор')
    weight = models.FloatField(verbose_name='Вес заказа в кг')
    region = models.IntegerField(verbose_name='Район доставки')
    delivery_hours = ArrayField(models.CharField(max_length=50,
                                                 verbose_name='Промежутки, в которые клиенту удобно принять заказ'))

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering = ['-region']
