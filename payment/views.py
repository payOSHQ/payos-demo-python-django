from rest_framework.views import APIView
from rest_framework.response import Response
import json
from config.utils import payOS
from datetime import datetime

class Payment(APIView):
    def post(self, request):
        try:
            data = request.data
            data = payOS.verifyPaymentWebhookData(data)

            if data.description in ['Ma giao dich thu nghiem', "VQRIO123"]:
                return Response({
                        "error": 0,
                        "message": "Ok",
                        "data": None
                    })

            return Response({
                        "error": 0,
                        "message": "Ok",
                        "data": None
                    })
        except Exception as e:
            print(e)
            return Response({
                "error": -1,
                "message": e,
                "data": None
                })