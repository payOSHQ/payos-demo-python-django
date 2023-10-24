from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order
from order.serializer import OrderSerializer
import os
import json
from config.utils import createSignatureFromObj
from datetime import datetime

class Payment(APIView):
    def post(self, request):
        try:
            data = request.data["data"]
            if(data is None):
                raise Exception("Không có dữ liệu") 
            if data["description"] == 'Ma giao dich thu nghiem':
                return Response({
                        "error": 0,
                        "message": "Ok",
                        "data": None
                    })
            signature = request.data["signature"]
            if signature is None:
                raise Exception("Không có chữ ký")
            
            signData = createSignatureFromObj(data=data, key=os.environ.get("PAYOS_CHECKSUM_KEY"))

            if signature != signData:
                raise Exception("Chữ ký không hợp lệ")
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