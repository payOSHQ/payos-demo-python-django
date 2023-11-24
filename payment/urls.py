
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payment.views import *
# 

urlpatterns = [
    path('payos_transfer_handler', Payment.as_view())
]
