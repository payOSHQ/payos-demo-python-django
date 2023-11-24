from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order
from order.serializer import OrderSerializer
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
            orderData = {
                "id": paymentData.orderCode,
                "items": json.dumps([i.__dict__ for i in paymentData.items], indent=2),
                "amount": paymentData.amount,
                "description": paymentData.description,
                "payment_link_id": payosCreateResponse["paymentLinkId"],
            }
            serializer = OrderSerializer(data=orderData)
            if serializer.is_valid():
                serializer.save()
            return Response({
                "error": 0,
                "message": "success",
                "data": {
                    "checkoutUrl": payosCreateResponse["checkoutUrl"]
                }
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
