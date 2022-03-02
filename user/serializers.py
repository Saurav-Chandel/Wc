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


#Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields="__all__" 



class RelatedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=('id','comment')               

class GetPostSerializer(serializers.ModelSerializer):
    post_comment=RelatedCommentsSerializer(many=True,read_only=True)
    class Meta:
        model=Post
        fields="__all__"        




class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields="__all__"   


class GetReplySerializer(serializers.ModelSerializer):
    comments=CommentsSerializer(read_only=True)
    class Meta:
        model=Reply
        fields="__all__" 

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model=Reply
        fields="__all__"         