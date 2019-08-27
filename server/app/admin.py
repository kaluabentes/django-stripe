from django.contrib import admin

from .models import Product
from .models import Order
from .models import CreditCard
from .models import SupportedDistrict
from .models import Option, OptionSection
from .models import Payment

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CreditCard)
admin.site.register(SupportedDistrict)
admin.site.register(Option)
admin.site.register(OptionSection)
admin.site.register(Payment)