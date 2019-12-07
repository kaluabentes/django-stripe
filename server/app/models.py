from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from .utils import get_app_config


def get_order_title(order_id, user):
    return "#" + str(order_id) + " by " + user.first_name + " " + user.last_name


class BaseProduct(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        abstract = True


class Option(BaseProduct):
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    chargeable = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class OptionSection(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    required = models.BooleanField(default=False)
    options = models.ManyToManyField(Option)

    def __str__(self):
        return self.title


class Product(BaseProduct):
    image = models.ImageField(upload_to='media', null=True, blank=True)
    option_sections = models.ManyToManyField(OptionSection)

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = get_app_config('order_status_steps')
    DEFAULT_STATUS = 'RECEIVED'

    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=DEFAULT_STATUS)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return get_order_title(self.id, self.user)


class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=150)
    number = models.CharField(max_length=16)
    exp_date = models.CharField(max_length=5)
    flag = models.CharField(max_length=50, null=True, blank=True)
    customer_id = models.CharField(max_length=50)

    def __str__(self):
        return str(self.flag) + " ****" + self.number[:4]


class SupportedDistrict(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Payment(models.Model):
    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    method = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return get_order_title(self.order.id, self.order.user)

