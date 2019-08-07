import os
import json
from functools import reduce

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

import stripe

from app.utils import parse_body
from app.models import Order
from app.models import Product
from app.models import UserCreditCard
from app.models import Payment
from app.models import Option

def create_payload_response(payload, status, message):
    return {"payload": payload, "status": status, "message": message}


class OrderView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderView, self).dispatch(request, *args, **kwargs)

    def sum_options_prices(self, options):
        total = 0

        for option in options:
            op = Option.objects.get(id=option['id'])
            
            if op.chargeable:
                total = total + (option['quantity'] * op.price)

        return total

    def sum_product_prices(self, products):
        total = 0

        for product in products:
            total = total + self.sum_options_prices(product['options']) + product['instance'].price
            print(product['instance'].price)

        return float(total)

    def post(self, request):
        # Create order
        payload = parse_body(request)
        user = User.objects.get(id=payload['user'])
        products = [
            {
                "instance": Product.objects.get(id=product["id"]), 
                "options": product["options"],
            } for product in payload["products"]
        ]
        order = Order(
            user=user,
        )
        order.save()

        for product in products:
            order.products.add(product["instance"])

        # Create payment
        user_credit_card = UserCreditCard.objects.get(id=payload["user_credit_card"])
        payment = Payment(
            order=order,
            user_credit_card=user_credit_card,
            value=self.sum_product_prices(products),
        )
        payment.save()

        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

        charge = stripe.Charge.create(
            amount=999,
            currency='usd',
            description='Example charge',
            source='tok_1F4KO3EFibI0APWSh37AlgyX',
        )

        response = create_payload_response({"order_id": order.id, "total": payment.value}, 201, "Created")
        return JsonResponse(response, status=201)
