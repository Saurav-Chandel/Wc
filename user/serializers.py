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



class ProfileSerializer(serializers.ModelSerializer):
    # following=FollowSerializer(read_only=True,many=True)
    # followers=FollowSerializer(read_only=True,many=True)
    profile_post=PostSerializer(read_only=True,many=True)
    class Meta:
        model=Profile
        fields="__all__"

from rest_framework.validators import UniqueTogetherValidator
# from rest_framework.validators import UniqueValidator
class FollowSerializer(serializers.ModelSerializer):

    profile_id=ProfileSerializer(read_only=True)
    following_profile_id=ProfileSerializer(read_only=True)

    class Meta:
        model=UserFollowing
        fields="__all__"


        # validators = [
           
        #     UniqueTogetherValidator(
        #         queryset=UserFollowing.objects.all(),
        #          fields=['profile_id', 'following_profile_id']
        #     )
        # ]

        # if validators:
        #     print("_____________")
        #     raise serializers.ValidationError("This field must be an even number.")


#Profile Serializer

