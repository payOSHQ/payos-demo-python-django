from rest_framework.views import APIView
from rest_framework.response import Response
import json
import random
from config.utils import payOS
from payos_lib_python import PaymentData, ItemData

# Create your views here.
class OrderCreate(APIView):
    def post(self, request):
        try:
            body = request.data
            item = ItemData(name= body["productName"], quantity=1, price=body["price"])

            paymentData = PaymentData(orderCode=random.randint(1000,99999), amount=body["price"], description=body["description"],\
                                      items=[item], cancelUrl= body["cancelUrl"], returnUrl= body["returnUrl"])

            payosCreateResponse = payOS.createPaymentLink(paymentData)
            return Response({
                "error": 0,
                "message": "success",
                "data": payosCreateResponse
            })
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
            data = payOS.getPaymentLinkInfomation(pk)
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
        
    def put(self, request, pk):
        try:
            order = payOS.cancelPaymentLink(pk)
            return Response(
                {
                    "error": 0,
                    "message": "Ok",
                    "data": order
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "error": -1,
                    "message": "Fail",
                    "data": None
                }
            )

class Webhook(APIView):
    def post(self, request):
        try:
            webhookUrl = request.data["webhook_url"]
            payOS.confirmWebhook(webhookUrl)
        except Exception as e:
            print(e)
            return Response(
                {
                    "error": -1,
                    "message": "Fail",
                    "data": None
                }
            )