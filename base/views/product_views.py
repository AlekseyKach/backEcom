from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import Product
from django.conf import settings
from django.contrib.auth.models import update_last_login, User
from django.contrib.auth.hashers import make_password
from base.serializers import ProductSerializer
from rest_framework import status


# get all products
@api_view(['GET'])
def GetProducts(requset):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
    

# get products by id
@api_view(['GET'])
def GetProductById(requset, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)
