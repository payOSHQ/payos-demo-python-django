from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order
from order.serializer import OrderSerializer
import json
from config.utils import payOS
from datetime import datetime

class Payment(APIView):
    def post(self, request):
        try:
            data = request.data
            # print(request.data)
            data = payOS.verifyPaymentWebhookData(data)
            if data["description"] in ['Ma giao dich thu nghiem', "VQRIO123"]:
                return Response({
                        "error": 0,
                        "message": "Ok",
                        "data": None
                    })

            order = Order.objects.get(pk=data["orderCode"])
            paymentData = {
                "status": "PAID",
                "ref_id": data["reference"],
                "transaction_when": datetime.strptime(data["transactionDateTime"], "%Y-%m-%d %H:%M:%S"),
                "transaction_code": data["code"],
                "webhook_snapshot": json.dumps(request.data)
            }
            serializer = OrderSerializer(order, data=paymentData, partial=True)
            if serializer.is_valid():
                serializer.save()
            else: raise Exception("Fail")
            return Response({
                        "error": 0,
                        "message": "Ok",
                        "data": paymentData
                    })
        except Exception as e:
            print(e)
            return Response({
                "error": -1,
                "message": e,
                "data": None
                })