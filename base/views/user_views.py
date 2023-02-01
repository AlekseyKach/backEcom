from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.models import update_last_login, User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from base.models import  User
from base.serializers import  UserSerializer, UserSerializerWithToken
from rest_framework import status


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

          

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def RegisterUser(request):
    data = request.data
    print('DATA',data)
   
    try:
        user = User.objects.create(
                first_name=data['name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password'])
            )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:   
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# update user profile ufter registeration
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateUserProfile(requset):
    user = requset.user
    serializer = UserSerializerWithToken(user, many=False)

    data = requset.data
    data.first_name=data['name'],
    data.username=data['email'],
    data.email=data['email'],
    
    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)

# get the loged user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserProfile(requset):
    user = requset.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# get all ussers that exist
@api_view(['GET'])
@permission_classes([IsAdminUser])
def GetUsers(requset):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
