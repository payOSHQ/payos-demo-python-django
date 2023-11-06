
from django.urls import path, include
from checkout.views import demo, Checkout, result
urlpatterns = [
    path('', demo),
    path('checkout', Checkout.as_view()),
    path('result', result)
]
