import json

from django.test import TestCase
from django.test import Client

from .models import Order

class OrderTestCase(TestCase):
    ORDER_PAYLOAD = {
        "user": 1,
        "user_credit_card": 3,
        "products": [
            {
                "id": 1,
                "quantity": 2,
                "options": [
                    {
                        "id": 1,
                        "quantity": 2,
                    }
                ]
            },
            {
                "id": 2,
                "quantity": 2,
                "options": [
                    {
                        "id": 1,
                        "quantity": 2,
                    }
                ]
            }
        ]
    }

    client = None

    def setUp(self):
        self.client = Client()

    def has_key(self, dict, key):
        if key in dict:
            return True
        return False

    def test_create_order(self):
        response = self.client.post('/api/v1/orders/')
        responseDict = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.has_key(responseDict['payload'], 'order_id'), True)