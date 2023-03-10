from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import Product ,Order,OrderItem,ShippingAddress
from django.contrib.auth.models import  User 
from django.contrib.auth.hashers import make_password
from base.serializers import  OrderSerializer

from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddOrderItem(request):
    user= request.user
    data=request.data
    
    
    orderItems= data['orderItems']    
    
    if orderItems and len(orderItems) == 0:
        return Response({'detail':'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # !!!Calls from frontend
        #   (1) Create order 
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice= data['shippingPrice'],
            totalPrice= data['totalPrice']
        )
        #   (2) create  shipping address
        shippingAddress = ShippingAddress.objects.create(
            order= order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )
        #   (3)  create order items add set order to order items relationship
        for  i in orderItems :
            product = Product.objects.get(_id=i['product'])
            
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['qty'],
                price = i['price'],
                image= product.image.url,
            )
            #   (4) Update Stock
            product.countInStock -= item.qty
            product.save()
        
        serializer = OrderSerializer (order,many=False)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetOrderById(requset,pk):
    try:
        user=requset.user
        order = Order.objects.get(_id=pk)
        # the user can only see  his order  unless is a admin user(staff)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order,many=False)
            return Response(serializer.data)
        else:
            Response({'detail':'Not authorized to view this Order'},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail':'order does not exist'} ,status=status.HTTP_400_BAD_REQUEST)   
    
    
    return