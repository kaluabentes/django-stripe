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
from app.models import CreditCard
from app.models import Payment
from app.models import Option


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class OrderView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def sum_options_prices(self, options):
        def sum_option_price(total, option):
            op = Option.objects.get(id=option['id'])
            if op.chargeable:
                return total + (option.get('quantity', 0) * op.price)
            return total

        return reduce(sum_option_price, options, 0)

    def sum_products_prices(self, products):
        def sum_product_price(total, product):
            return total + self.sum_options_prices(product['options']) + product['instance'].price

        return float(reduce(sum_product_price, products, 0))

    def format_price(self, price):
        return int(round(price * 100, 0))

    def post(self, request):
        # Create order
        body = parse_body(request)
        user = User.objects.get(id=body['user'])
        products = [
            {
                "instance": Product.objects.get(id=product["id"]),
                "options": product["options"],
            } for product in body["products"]
        ]
        order = Order(
            user=user,
        )
        order.save()
        for product in products:
            order.products.add(product["instance"])
        payment = Payment(
            order=order,
            method='Credit card',
            value=self.sum_products_prices(products),
        )
        payment.save()
        charge = stripe.Charge.create(
            amount=self.format_price(self.sum_products_prices(products)),
            currency='usd',
            description='Order #' + str(order.id),
            customer=user.creditcard.customer_id,
        )
        response = {
            "id": order.id,
            "total": payment.value
        }

        return JsonResponse(response, status=201)


class CreditCardView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        body = parse_body(request)
        user = User.objects.get(id=body['user'])
        credit_card_exists = CreditCard.objects.filter(user=user.id).exists()

        if credit_card_exists:
            credit_card = CreditCard.objects.get(user=user.id)
            credit_card.name = body['name']
            credit_card.number = body['number']
            credit_card.exp_date = body['exp_date']
            credit_card.save()
            customer = stripe.Customer.modify(
                credit_card.customer_id, source=body['token'])
        else:
            customer = stripe.Customer.create(
                source=body['token'],
                email=user.email
            )
            credit_card = CreditCard(
                customer_id=customer.id,
                user=user,
                name=body['name'],
                number=body['number'],
                exp_date=body['exp_date']
            )
            credit_card.save()

        response = {
            "id": credit_card.id,
            "customer_id": customer.id,
        }

        return JsonResponse(response, status=201)
