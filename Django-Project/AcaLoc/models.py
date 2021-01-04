from django.db import models
from django import template
register = template.Library()

@register.filter()
def class_name(value):
    return value.__class__.__name__

class Department(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField(max_length=30)
    longitude = models.FloatField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s" % self.name


class Academican(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MarketPlace(models.Model):
    name = models.CharField(max_length=30)
    location = models.FloatField(max_length=30)

    def __str__(self):
        return self.name


class Shops(models.Model):
    name = models.CharField(max_length=30)
    tag = models.CharField(max_length=30)
    contact = models.CharField(max_length=11)
    market_place = models.ForeignKey(MarketPlace, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
