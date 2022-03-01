from .models import *
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"


    def create(self,validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

        extra_kwargs = {
            "password": {"write_only": True},
        } 



