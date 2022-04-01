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
        print('_________')

    def create(self,validated_data):
        print("+++++++++++++")
        c = Comments.objects.create(
            post=validated_data['post'],
            user=validated_data['user'],
            comment=validated_data['comment'],
            like=validated_data['like'],
            # created_at=validated_data['created_at']
        )
        c.save()
        print(c.id)
        notification=UserNotifications.objects.create(User_id=c.user,post=c.post)
        print(notification)
        notification.save()
        return c

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


from django.db.models import Count
class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(method_name='followings')
    follower = serializers.SerializerMethodField(method_name='followers')
    # following=FollowSerializer(read_only=True,many=True)
    # followers=FollowSerializer(read_only=True,many=True)
    profile_post=PostSerializer(read_only=True,many=True)
    class Meta:
        model=Profile
        fields="__all__"

    #serializer method to find the followings of particular user.
    def followings(self,obj):
        queryset=UserFollowing.objects.filter(profile_id=obj.id).aggregate(Count('following_profile_id')) 
        return queryset
    
    #serializer method to find the followers of particular user.
    def followers(self,obj):
        queryset=UserFollowing.objects.filter(following_profile_id=obj.id).aggregate(Count('profile_id')) 
        return queryset


from rest_framework.validators import UniqueTogetherValidator
# from rest_framework.validators import UniqueValidator
class FollowSerializer(serializers.ModelSerializer):

    # profile_id=ProfileSerializer(read_only=True)
    # following_profile_id=ProfileSerializer(read_only=True)

    class Meta:
        model=UserFollowing
        fields="__all__"

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=UserFollowing.objects.all(),
        #          fields=['profile_id', 'following_profile_id']
        #     )
        # ]


    def validate(self,validated_data):
        profile_id=validated_data['profile_id']  
        print(profile_id)
        following_profile_id=validated_data['following_profile_id']
        if profile_id == following_profile_id:
            raise serializers.ValidationError("you can not follow itself")
        return validated_data

#Profile Serializer
class UserNotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserNotifications
        fields="__all__"


class CommentSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model=CommentSettings
        fields="__all__"

