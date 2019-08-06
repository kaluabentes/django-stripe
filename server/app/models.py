from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from .utils import get_app_config


def get_order_title(order_id, user):
    return "#" + str(order_id) + " by " + user.first_name + " " + user.last_name


class BaseProduct(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        abstract = True


class Option(BaseProduct):
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


class UserCreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    fast_name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    number = models.CharField(max_length=16)
    exp_date = models.CharField(max_length=5)
    flag = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return str(self.flag) + " ****" + self.number[:4]


class SupportedDistrict(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    user_credit_card = models.ForeignKey(UserCreditCard, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return get_order_title(self.order.id, self.user_credit_card.user)
