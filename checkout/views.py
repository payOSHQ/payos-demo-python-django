from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from config.utils import payOS
from payos_lib_python import PaymentData, ItemData

def index(request):
    return render(request, "index.html",)

def success(request):
    return render(request, "success.html",)

def cancel(request):
    return render(request, "cancel.html",)

class Checkout(APIView):
    def post(self, request):
        try:
            item = ItemData(name= "Mì tôm hảo hảo ly", quantity=1, price= 1000)
            paymentData = PaymentData(orderCode=random.randint(1000,99999), amount=1000, description="Thanh toán đơn hàng",\
                items=[item], cancelUrl= "http://localhost:8000/cancel", returnUrl= "http://localhost:8000/success")

            payosCreateResponse = payOS.createPaymentLink(paymentData)
            return redirect(payosCreateResponse.checkoutUrl)

        except Exception as e:
            print(e)
            return render(request, "index.html",)
