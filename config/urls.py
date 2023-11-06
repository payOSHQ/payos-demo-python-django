
from django.urls import path, include

urlpatterns = [
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('', include('checkout.urls'))
]
