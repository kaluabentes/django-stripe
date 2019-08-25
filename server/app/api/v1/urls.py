from django.urls import path

from .views import OrderView
from .views import CreditCardView


urlpatterns = [
    path("orders/", OrderView.as_view()),
    path("creditcards/", CreditCardView.as_view()),
]
