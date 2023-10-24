from django.db import models
from django.utils import timezone


class Order(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    status = models.CharField(max_length=8, default="PENDING", null=False)
    items = models.CharField(max_length=255, null=False)
    amount = models.IntegerField(null=False)
    ref_id = models.CharField(max_length=30, null= True)
    description = models.CharField(max_length=255, null=False)
    transaction_when = models.DateTimeField(null=True)
    payment_link_id = models.CharField(max_length=255, null=True)
    transaction_code = models.CharField(max_length=6, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    webhook_snapshot = models.TextField(max_length=65535, null=True)

    class Meta:
        db_table = 'order'
        managed = False
