from django.urls import path

from .views import OrdersView
from .views import CreditCardsView
from .views import ProductsView


urlpatterns = [
    path("orders/", OrdersView.as_view()),
    path("creditcards/", CreditCardsView.as_view()),
    path("products/", ProductsView.as_view()),
]
