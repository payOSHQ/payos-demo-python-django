from rest_framework import serializers
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    # transaction_when = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs ={
            "status": {'required': False},
            "ref_id": {'required': False},
            "transaction_when": {'required': False},
            "transaction_code": {'required': False},
            "updated_at": {'required': False},
            "webhook_snapshot": {'required': False},
        }
