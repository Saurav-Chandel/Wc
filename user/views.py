from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt import authentication
from .serializers import *
from .models import *
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# Create your views here.

class SignUpView(APIView):
    permission_class = [permissions.AllowAny]
    authentication_classes = []

    def post(self,request):
        data=request.data
        print(data)
        

        if User.objects.filter(email=request.data['email']).exists():
            return Response({"error_message":"Email Already Exist"})

        else:
            data['username']=data['email']     #if input is from json in postman this is right approach .("if the data is dictionary format")

            serializer=SignUpSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "data":serializer.data,
                    "code": status.HTTP_200_OK,
                    "message": "User created successfully",
                })
            else:
                return Response({
                    "data":serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Serializer.error",
                })        


from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

class SigninView(APIView):
    permission_class = [permissions.AllowAny]
    authentication_classes = []

    def post(self,request):
        if 'email' in request.data and 'password' in request .data:
            data=request.data
            email=data['email']
            password=data['password']
            print(data)

            try:
                user=User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"data": None,"message": "User Does Not Exist"},status = status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                token=RefreshToken.for_user(user)
                if not Token.objects.filter(token_type="access_token", user_id=user.id).exists():
                     Token.objects.create(
                        user_id=user.id,
                        token=str(token.access_token),
                        token_type="access_token",
                    )
                else:
                    Token.objects.filter(
                        user_id=user.id, token_type="access_token"
                    ).update(token=str(token.access_token))    

                serializer=LoginSerializer(user) 

                return Response(
                    {
                        "data": serializer.data,
                        "access_token": str(token.access_token),
                        "refresh_token": str(token),
                        "code": status.HTTP_200_OK,
                        "message": "Login SuccessFully",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "data": "wrong credentials",
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Serializer error",
                    }
                )   
        else:
            return Response(
                    {
                        "data": "please enter email or password",
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Serializer error",
                    }
                )   


# class Forgotpassword(APIView):
#     permission_class = [permissions.AllowAny]
#     authentication_classes = []

#     def post(self,request):
#         data=request.data
#         email=data['email']












                


           
           








