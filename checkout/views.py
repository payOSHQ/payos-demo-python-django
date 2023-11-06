from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import random
from config.utils import createSignatureOfPaymentRequest, createSignatureFromObj
import os
import requests

def index(request):
    return render(request, "index.html",)

def success(request):
    return render(request, "success.html",)

def cancel(request):
    return render(request, "cancel.html",)

class Checkout(APIView):
    def post(self, request):
        try:
            bodyRequest = {
                "orderCode": random.randint(1000,99999),
                "amount": 1000,
                "description": "Thanh toán đơn hàng",
                "items": [{
                    "name": "Mì tôm hảo hảo ly",
                    "quantity": 1,
                    "price": 1000
                }],
                "cancelUrl": "http://localhost:8000/cancel",
                "returnUrl": "http://localhost:8000/success"
            }
            key = os.environ.get("PAYOS_CHECKSUM_KEY")
            bodyToSignature = createSignatureOfPaymentRequest(bodyRequest, key)
            bodyRequest["signature"] = bodyToSignature
            url = os.environ.get("PAYOS_CREATE_PAYMENT_LINK_URL")
            
            headers = {
                "Content-Type": "application/json",  # Loại nội dung của body
                "x-client-id": os.environ.get("PAYOS_CLIENT_ID"),
                "x-api-key": os.environ.get("PAYOS_API_KEY"),
            }

            response = requests.post(url, json=bodyRequest, headers=headers)

            if response.status_code == 200:
                paymentLinkRes = response.json()
                if(paymentLinkRes["code"] == "00"):
                    paymentLinkResSignature = createSignatureFromObj(paymentLinkRes["data"], key)

                    if paymentLinkResSignature != paymentLinkRes["signature"]:
                        raise Exception("Fail")
                    
                    return redirect(paymentLinkRes["data"]["checkoutUrl"])
            else:
                raise Exception("HTTP error!")

        except Exception as e:
            print(e)
            return render(request, "demo.html",)
