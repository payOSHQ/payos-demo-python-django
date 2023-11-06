from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order
from order.serializer import OrderSerializer
import json
import random
from config.utils import createSignatureOfPaymentRequest, createSignatureFromObj
import os
import requests

# Create your views here.

class OrderCreate(APIView):
    def post(self, request):
        try:
            body = request.data
            bodyRequest = {
                "orderCode": random.randint(1000,99999),
                "amount": body["price"],
                "description": body["description"],
                "items": [{
                    "name": body["productName"],
                    "quantity": 1,
                    "price": body["price"]
                }],
                "cancelUrl": body["cancelUrl"],
                "returnUrl": body["returnUrl"]
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
            print(response.json())
            if response.status_code == 200:
                paymentLinkRes = response.json()
                if(paymentLinkRes["code"] == "00"):
                    paymentLinkResSignature = createSignatureFromObj(paymentLinkRes["data"], key)
                    if paymentLinkResSignature != paymentLinkRes["signature"]:
                        raise Exception("Fail")
                    orderData = {
                        "id": bodyRequest["orderCode"],
                        "items": json.dumps(bodyRequest["items"]),
                        "amount": bodyRequest["amount"],
                        "description": bodyRequest["description"],
                        "payment_link_id": paymentLinkRes["data"]["paymentLinkId"],
                        # "ref_id": None,
                        # "transaction_when": None,
                        # "transaction_code": None,
                        # "updated_at": None,
                        # "webhook_snapshot": None
                    }
                    serializer = OrderSerializer(data=orderData)
                    if serializer.is_valid():
                        serializer.save()
                    return Response({
                        "error": 0,
                        "message": paymentLinkRes["desc"],
                        "data": {
                            "checkoutUrl": paymentLinkRes["data"]["checkoutUrl"]
                        }
                    })
                else: 
                    raise Exception("HTTP error!")

            else:
                raise Exception("HTTP error!")

        except Exception as e:
            print(e)
            return Response({
                "error": -1,
                "message": "Fail",
                "data": None
                })
       

class OrderManage(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            data = serializer.data
            data["items"] = json.loads(data["items"])
            if data["webhook_snapshot"] is not None:
                data["webhook_snapshot"] = json.loads(data["webhook_snapshot"])
            return Response(
                {
                    "error": 0,
                    "message": "Ok",
                    "data": data
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "error": -1,
                    "message": "Product does not exist",
                    "data": None
                }
            )
