from re import S
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt import authentication
from .serializers import *
from .models import *
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .responses import ResponseBadRequest, ResponseNotFound, ResponseOk


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FormParser, MultiPartParser

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


from django.db.models import Q

class GetAllProfile(APIView):
    """
    Get lis of profile
    """
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    search = openapi.Parameter('search',
                            in_=openapi.IN_QUERY,
                            description='Search other profiles ',
                            type=openapi.TYPE_STRING,
                            )

    post_id = openapi.Parameter('post_id',
                            in_=openapi.IN_QUERY,
                            description='find all posts on the basis of post id',
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_INTEGER)
                            )                        
    @swagger_auto_schema(
            manual_parameters=[search,post_id]
    )                        

    @csrf_exempt
    def get(self, request):
        try:
            data=request.GET
            if data.get('search'):
                search=data.get('search')
            else:
                search=data.get('search')    

            if data.get('post_id'):
                post_id=data.get('post_id')
            else:
                post_id=data.get('post_id')     

            profile=Profile.objects.all()

            if search:
                profile=profile.filter(Q(user__first_name__icontains=search))

            # if post_id:
            #     profile1=Post.objects.filter(posted_by=post_id)  
            #     print(profile1) 
            #     return ResponseOk({"data":profile1.data}) 

            if profile:    
                serializer=ProfileSerializer(profile,many=True) 
                return ResponseOk({
                    'data':serializer.data,
                    'status':status.HTTP_200_OK,
                    'msg':'All Profile List'
                })  
            else:
                return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"search query does not find"
            }) 

        except:
            return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"Profile list does not exists"
            })      

class CreateProfile(APIView):
    """
    Create Profile
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="create Profile",
        request_body=ProfileSerializer,
    )

    @csrf_exempt
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # user_obj=User.objects.filter(id=user_obj.id)[0]
            # user_serializer=UserSerializer(user_obj)
            # print(user_serializer)

            return Response(
                {
                    "data": serializer.data,
                    # "user_id":GetProfileSerializer(),
                    "code": status.HTTP_200_OK,
                    "message": "Profile created succesfully",
                }
            )
        else:    
            return Response(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Profile is not valid",
                }
            )

class UpdateProfile(APIView):
    """
    Update Profile
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="update Profile",
        request_body=ProfileSerializer,
    )
    @csrf_exempt
    def patch(self,request,pk):
        try:
            profile=self.get_object(pk)
            serializer=ProfileSerializer(profile,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data":serializer.data,
                        "code":status.HTTP_200_OK,
                        "message":"Profile updated successfully"
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data":serializer.errors,
                        "code":status.HTTP_400_BAD_REQUEST,
                        "message":"Profile Not Valid"
                    }
                )  
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Profile Does Not exists."
                }
            )          

class GetProfile(APIView):
    """
    Get Profile by id
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

   
    def get(self,request,pk):
        try:
            profile=self.get_object(pk)
            serializer=ProfileSerializer(profile)
            return ResponseOk(
                {
                    "data":serializer.data,
                    "code":status.HTTP_200_OK,
                    "message":"Get Profile successfully"
                }
            )
           
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Profile Does Not exists."
                }
            )    

class DeleteProfile(APIView):
    """
    Delete Profile
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]


    @csrf_exempt
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            profile = self.get_object(pk)
            profile.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Profile deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Profile Does Not Exist",
                }
            )


class GetAllCategory(APIView):
    """
    Get All category
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    @csrf_exempt
    def get(self, request):
        try:
            data=request.GET
            category=Category.objects.all()
            serializer=CategorySerializer(category,many=True) 
            return ResponseOk({
                'data':serializer.data,
                'status':status.HTTP_200_OK,
                'msg':'All Category List'
            })                 
        except:
            return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"Category list does not exists"
            })      
from main import settings
class CreateCategory(APIView):
    """
    Create Category
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    # parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="creater Category API",
        operation_summary="creater Category API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "cat_name": openapi.Schema(type=openapi.TYPE_STRING),
                "created_at": openapi.Schema(type=openapi.TYPE_STRING,format=settings.FORMAT_DATE)
            },
        ),
    )

    @csrf_exempt
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # user_obj=User.objects.filter(id=user_obj.id)[0]
            # user_serializer=UserSerializer(user_obj)
            # print(user_serializer)

            return Response(
                {
                    "data": serializer.data,
                    # "user_id":GetProfileSerializer(),
                    "code": status.HTTP_200_OK,
                    "message": "Category created succesfully",
                }
            )
        else:    
            return Response(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Category is not valid",
                }
            )

class UpdateCategory(APIView):
    """
    Update Category
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

    # @swagger_auto_schema(
    #     operation_description="update Profile",
    #     request_body=CategorySerializer,
    # )
    @csrf_exempt
    def put(self,request,pk):
        try:
            category=self.get_object(pk)
            serializer=CategorySerializer(category,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data":serializer.data,
                        "code":status.HTTP_200_OK,
                        "message":"category updated successfully"
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data":serializer.errors,
                        "code":status.HTTP_400_BAD_REQUEST,
                        "message":"category Not Valid"
                    }
                )  
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"category Does Not exists."
                }
            )          

class GetCategory(APIView):
    """
    Get category by id
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise ResponseNotFound()

   
    def get(self,request,pk):
        try:
            category=self.get_object(pk)
            serializer=CategorySerializer(category)
            return ResponseOk(
                {
                    "data":serializer.data,
                    "code":status.HTTP_200_OK,
                    "message":"Get Category successfully"
                }
            )
           
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"category Does Not exists."
                }
            )    

class DeleteCategory(APIView):
    """
    Delete Category
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]


    @csrf_exempt
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            category = self.get_object(pk)
            category.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "category deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "category Does Not Exist",
                }
            )


from django.forms.models import model_to_dict
class GetAllPost(APIView):
    """
    Get All post
    """
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    category = openapi.Parameter('category',
                            in_=openapi.IN_QUERY,
                            description='filter post on the basis of category',
                            type=openapi.TYPE_STRING,
                            )

    @swagger_auto_schema(
            manual_parameters=[category]
    )                       

    @csrf_exempt
    def get(self, request):
        try:
            data=request.GET

            if data.get('category'):
                category=data.get('category')
            else:
                category=data.get('category')

            post=Post.objects.all()

            if category:
                post=post.filter(Q(category__cat_name__icontains=category))

            if post:    
                serializer=GetPostSerializer(post,many=True) 
                
                return ResponseOk({
                    'data':serializer.data,
                    'status':status.HTTP_200_OK,
                    'msg':'All post List'
                })  
            else:
                return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"category does not found"
            })  

        except:
            return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"post list does not exists"
            })      

class CreatePost(APIView):
    """
    Create Post
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="Create Post",
        request_body=PostSerializer,
    )

    @csrf_exempt
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # user_obj=User.objects.filter(id=user_obj.id)[0]
            # user_serializer=UserSerializer(user_obj)
            # print(user_serializer)

            return Response(
                {
                    "data": serializer.data,
                    # "user_id":GetProfileSerializer(),
                    "code": status.HTTP_200_OK,
                    "message": "Post created succesfully",
                }
            )
        else:    
            return Response(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Post is not valid",
                }
            )

class UpdatePost(APIView):
    """
    Update Post
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="update Post",
        request_body=PostSerializer,
    )
    @csrf_exempt
    def put(self,request,pk):
        try:
            post=self.get_object(pk)
            serializer=PostSerializer(post,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data":serializer.data,
                        "code":status.HTTP_200_OK,
                        "message":"Post updated successfully"
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data":serializer.errors,
                        "code":status.HTTP_400_BAD_REQUEST,
                        "message":"Post Not Valid"
                    }
                )  
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Post Does Not exists."
                }
            )          

class GetPost(APIView):
    """
    Get Post by id
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise ResponseNotFound()

   
    def get(self,request,pk):
        try:
            post=self.get_object(pk)
            serializer=GetPostSerializer(post)
            return ResponseOk(
                {
                    "data":serializer.data,
                    "code":status.HTTP_200_OK,
                    "message":"Get Post successfully"
                }
            )
           
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Post Does Not exists."
                }
            )    

class DeletePost(APIView):
    """
    Delete Post
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]


    @csrf_exempt
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            post = self.get_object(pk)
            post.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Post deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Post Does Not Exist",
                }
            )
                

class GetAllComment(APIView):
    """
    Get All Comment
    """
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.JWTAuthentication]

    
    post_id = openapi.Parameter('post_id',
                            in_=openapi.IN_QUERY,
                            description='find the all comments related to a particular post',
                            type=openapi.TYPE_STRING,
                            )  

    @swagger_auto_schema(
            manual_parameters=[post_id]
    )                        

    @csrf_exempt
    def get(self, request):
        try:
            data=request.GET
            if data.get('post_id'):
                post_id=data.get('post_id')
            else:
                post_id=""

            comment=Comments.objects.all()
            if post_id:
                comment=comment.filter(post=post_id)
                total_comment=Comments.objects.filter(post=post_id).count()
                total_likes=Comments.objects.filter(post=post_id,like=True).count()

                return ResponseOk({
                    'data':comment.values(),
                    'total_comments':total_comment,
                    'total_likes':total_likes,
                    'status':status.HTTP_200_OK,
                    'msg':'All Comment List'
                }) 

            if comment:
                serializer=CommentsSerializer(comment,many=True) 
                
                return ResponseOk({
                    'data':serializer.data,
                    # 'total_comment':total_comment,
                    'status':status.HTTP_200_OK,
                    'msg':'All Comment List'
                })  
            else:
                return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"query does not found"
            }) 
        except:
            return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"Comment list does not exists"
            })      

class CreateComment(APIView):
    """
    Create Comment
    """ 

    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    # parser_classes = (FormParser, MultiPartParser)
    
    @swagger_auto_schema(
        operation_description="creater Category API",
        operation_summary="creater Category API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "post": openapi.Schema(type=openapi.TYPE_INTEGER),
                "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                "comment": openapi.Schema(type=openapi.TYPE_STRING),
                "like": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                # "created_at": openapi.Schema(type=openapi.TYPE_STRING,format=settings.FORMAT_DATE)
            },
        ),
    )

    @csrf_exempt
    def post(self, request):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data": serializer.data,
                    # "user_id":GetProfileSerializer(),
                    "code": status.HTTP_200_OK,
                    "message": "Comment created succesfully",
                }
            )
        else:    
            return Response(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Post is not valid",
                }
            )

class UpdateComment(APIView):
    """
    Update Comment
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    # parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_description="creater Category API",
        operation_summary="creater Category API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "post": openapi.Schema(type=openapi.TYPE_INTEGER),
                "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                "comment": openapi.Schema(type=openapi.TYPE_STRING),
                "like": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "created_at": openapi.Schema(type=openapi.TYPE_STRING,format=settings.FORMAT_DATE)
            },
        ),
    )

    def get_object(self, pk):
        try:
            return Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            raise ResponseNotFound()

    @swagger_auto_schema(
        operation_description="update Post",
        request_body=PostSerializer,
    )
    @csrf_exempt
    def put(self,request,pk):
        try:
            comment=self.get_object(pk)
            serializer=CommentsSerializer(comment,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseOk(
                    {
                        "data":serializer.data,
                        "code":status.HTTP_200_OK,
                        "message":"Comment updated successfully"
                    }
                )
            else:
                return ResponseBadRequest(
                    {
                        "data":serializer.errors,
                        "code":status.HTTP_400_BAD_REQUEST,
                        "message":"Comment Not Valid"
                    }
                )  
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Comment Does Not exists."
                }
            )          

class GetComment(APIView):
    """
    Get Comment by id
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get_object(self, pk):
        try:
            return Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            raise ResponseNotFound()

   
    def get(self,request,pk):
        try:
            comment=self.get_object(pk)
            serializer=CommentsSerializer(comment)
            return ResponseOk(
                {
                    "data":serializer.data,
                    "code":status.HTTP_200_OK,
                    "message":"Get comment successfully"
                }
            )
           
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Comment Does Not exists."
                }
            )    

class DeleteComment(APIView):
    """
    Delete Comment
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]


    @csrf_exempt
    def get_object(self, pk):
        try:
            return Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            raise ResponseNotFound()

    def delete(self, request, pk):
        try:
            comment = self.get_object(pk)
            comment.delete()
            return ResponseOk(
                {
                    "data": None,
                    "code": status.HTTP_200_OK,
                    "message": "Comment deleted Successfully",
                }
            )
        except:
            return ResponseBadRequest(
                {
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Comment Does Not Exist",
                }
            )           



class GetAllReply(APIView):
    """
    Get All Reply
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    # post_id = openapi.Parameter('post_id',
    #                         in_=openapi.IN_QUERY,
    #                         description='find the all comments related to a particular post',
    #                         type=openapi.TYPE_STRING,
    #                         )  

    # @swagger_auto_schema(
    #         manual_parameters=[post_id]
    # )                        

    @csrf_exempt
    def get(self, request):
        try:
            data=request.GET
            # if data.get('post_id'):
            #     post_id=data.get('post_id')
            # else:
            #     post_id=""

            post=Reply.objects.all()

            # if post_id:
            #     post=post.filter(post=post_id)

            # if post:
            serializer=GetReplySerializer(post,many=True) 
            
            return ResponseOk({
                'data':serializer.data,
                'status':status.HTTP_200_OK,
                'msg':'All Reply List'
            })  
            # else:
            #     return ResponseBadRequest({
            #     "data":None,
            #     "status":status.HTTP_400_BAD_REQUEST,
            #     "msg":"query does not found"
            # }) 
        except:
            return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"Reply list does not exists"
            })      

class CreateReply(APIView):
    """
    Create Reply
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    # parser_classes = (FormParser, MultiPartParser)
    
    @swagger_auto_schema(
        operation_description="create Reply API",
        operation_summary="create Replys API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "commets": openapi.Schema(type=openapi.TYPE_INTEGER),
                "reply": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )

    @csrf_exempt
    def post(self, request):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data": serializer.data,
                    # "user_id":GetProfileSerializer(),
                    "code": status.HTTP_200_OK,
                    "message": "Reply created succesfully",
                }
            )
        else:    
            return Response(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Reply is not valid",
                }
            )

# class UpdateComment(APIView):
#     """
#     Update Comment
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [authentication.JWTAuthentication]
#     # parser_classes = (FormParser, MultiPartParser)

#     @swagger_auto_schema(
#         operation_description="creater Category API",
#         operation_summary="creater Category API",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "post": openapi.Schema(type=openapi.TYPE_INTEGER),
#                 "user": openapi.Schema(type=openapi.TYPE_INTEGER),
#                 "comment": openapi.Schema(type=openapi.TYPE_STRING),
#                 "like": openapi.Schema(type=openapi.TYPE_BOOLEAN),
#                 "created_at": openapi.Schema(type=openapi.TYPE_STRING,format=settings.FORMAT_DATE)
#             },
#         ),
#     )

#     def get_object(self, pk):
#         try:
#             return Comments.objects.get(pk=pk)
#         except Comments.DoesNotExist:
#             raise ResponseNotFound()

#     @swagger_auto_schema(
#         operation_description="update Post",
#         request_body=PostSerializer,
#     )
#     @csrf_exempt
#     def put(self,request,pk):
#         try:
#             comment=self.get_object(pk)
#             serializer=CommentsSerializer(comment,data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return ResponseOk(
#                     {
#                         "data":serializer.data,
#                         "code":status.HTTP_200_OK,
#                         "message":"Comment updated successfully"
#                     }
#                 )
#             else:
#                 return ResponseBadRequest(
#                     {
#                         "data":serializer.errors,
#                         "code":status.HTTP_400_BAD_REQUEST,
#                         "message":"Comment Not Valid"
#                     }
#                 )  
#         except:
#             return  ResponseBadRequest(
#                 {
#                     "data":None,
#                     "code":status.HTTP_400_BAD_REQUEST,
#                     "message":"Comment Does Not exists."
#                 }
#             )          

# class GetComment(APIView):
#     """
#     Get Comment by id
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [authentication.JWTAuthentication]

#     def get_object(self, pk):
#         try:
#             return Comments.objects.get(pk=pk)
#         except Comments.DoesNotExist:
#             raise ResponseNotFound()

   
#     def get(self,request,pk):
#         try:
#             comment=self.get_object(pk)
#             serializer=CommentsSerializer(comment)
#             return ResponseOk(
#                 {
#                     "data":serializer.data,
#                     "code":status.HTTP_200_OK,
#                     "message":"Get comment successfully"
#                 }
#             )
           
#         except:
#             return  ResponseBadRequest(
#                 {
#                     "data":None,
#                     "code":status.HTTP_400_BAD_REQUEST,
#                     "message":"Comment Does Not exists."
#                 }
#             )    

# class DeleteComment(APIView):
#     """
#     Delete Comment
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [authentication.JWTAuthentication]


#     @csrf_exempt
#     def get_object(self, pk):
#         try:
#             return Comments.objects.get(pk=pk)
#         except Comments.DoesNotExist:
#             raise ResponseNotFound()

#     def delete(self, request, pk):
#         try:
#             comment = self.get_object(pk)
#             comment.delete()
#             return ResponseOk(
#                 {
#                     "data": None,
#                     "code": status.HTTP_200_OK,
#                     "message": "Comment deleted Successfully",
#                 }
#             )
#         except:
#             return ResponseBadRequest(
#                 {
#                     "data": None,
#                     "code": status.HTTP_400_BAD_REQUEST,
#                     "message": "Comment Does Not Exist",
#                 }
#             ) 


#ManyToMany followers and following in profile Model.

class AddFollower(APIView):
    '''
    Add follower
    '''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def post(self,request):
        data=request.data
    
        jo_follow_kr_raha_hai = Profile.objects.get(id=data.get('jo_follow_kr_raha_hai_id'))   #srv follows grv and srv's following added gaurav.
        jisko_follow_kiya =  Profile.objects.get(id=data.get('jisko_follow_kiya_id'))    #grv is followed by srv and srv is follower of grv.

        jo_follow_kr_raha_hai.following.add(jisko_follow_kiya)
        jo_follow_kr_raha_hai.save()

        jisko_follow_kiya.followers.add(jo_follow_kr_raha_hai)
        jisko_follow_kiya.save()

        print(str(jo_follow_kr_raha_hai) + "follows" + str(jisko_follow_kiya) )

        return Response({'status':status.HTTP_200_OK,
                         "data":"",
                         "message":str(jo_follow_kr_raha_hai.first_name) +" "+ "follows" +" "+ str(jisko_follow_kiya.first_name)})

#post man API
class AddFollowing(APIView):
    '''
    add following
    '''

    def post(self,request):
        data=request.data
        if data:

           jo_follow_kr_raha_hai=Profile.objects.get(id=data.get('jo_follow_kr_raha_hai_id')) 
           jisko_follow_kiya=Profile.objects.get(id=data.get('jisko_follow_kiya_id')) 

           u=UserFollowing.objects.filter(profile_id=data.get('jo_follow_kr_raha_hai_id'))
           uu=UserFollowing.objects.filter(following_profile_id=data.get('jisko_follow_kiya_id'))

           if data.get('jo_follow_kr_raha_hai_id') == data.get('jisko_follow_kiya_id'):
               return Response({"msg":"you can not follow itself"})
           else:    
                print(len(UserFollowing.objects.filter(profile_id=data.get('jo_follow_kr_raha_hai_id'))))
                print(len(UserFollowing.objects.filter(following_profile_id=data.get('jisko_follow_kiya_id'))))
     
                if len(u)>=1 and len(uu)>=1: 
                    return Response({"msg":"you already followed this user"})
                else:

                     UserFollowing.objects.create(profile_id=jo_follow_kr_raha_hai,
                                       following_profile_id=jisko_follow_kiya)
             
                     return Response({'status':status.HTTP_200_OK,
                                      "data":"",
                                      "message":str(jo_follow_kr_raha_hai) +" "+ "follows" +" "+ str(jisko_follow_kiya)})
        return Response({"msg":"enter a input value"})


class GetAllFollow(APIView):
    '''
    List of All follows
    '''
    #user who follows the other user(jo follow kr rha hai)
    profile_id = openapi.Parameter('profile_id',
                            in_=openapi.IN_QUERY,
                            description='enter the profile_id',
                            type=openapi.TYPE_STRING,
                            )  

    #jis jis ko follow kiya un sbki id.
    # post_id_array = openapi.Parameter('post_id_array',
    #                         in_=openapi.IN_QUERY,
    #                         description='find all posts on the basis of post id',
    #                         type=openapi.TYPE_ARRAY,
    #                         items=openapi.Items(type=openapi.TYPE_INTEGER)
    #                         )                        

    @swagger_auto_schema(
            manual_parameters=[profile_id]
    )

    @csrf_exempt
    def get(self,request):
        try:
            data=request.GET
            # if data.get('post_id_array'):
            #    post_id_array=data.get('post_id_array')
            #    post_id_array=post_id_array.split(",")
            # else:
            #    post_id_array=""

            # print(post_id_array)   

            if data.get('profile_id'):
               profile=data.get('profile_id')
            else:
               profile=""   

            print(profile)   

            follow=UserFollowing.objects.all()
            # print(follow)
            # if profile:
            #     follow=follow.filter(profile_id=profile)  #filter all the profiles which is followed by particular user.  
            #     print(follow)

            if profile:
                follow=follow.filter(profile_id=profile).values('following_profile_id')
                # follow=follow.filter(following_profile_id__in=follow1).values('following_profile_id')  #get id of those person who is followed by particular person.
        
                post=Post.objects.filter(posted_by__in=follow).values() #filter all the posts based on following id's.
                
                if post:
                    return ResponseOk({
                            'data':post,
                            'status':status.HTTP_200_OK,
                            'msg':'list of all posts of followwd person'
                        })
                else:
                    return ResponseBadRequest({
                    "data":None,
                    "status":status.HTTP_400_BAD_REQUEST,
                    "msg":"UserFollowing list does not exists"
                })         

            if follow:
                serializer=FollowSerializer(follow,many=True)
            
                return ResponseOk({
                        'data':serializer.data,
                        'status':status.HTTP_200_OK,
                        'msg':'All UserFollowing List'
                    })  
            else:
                return Response({"msg":"error"})        
 
        except:
            return ResponseBadRequest({
                "data":None,
                "status":status.HTTP_400_BAD_REQUEST,
                "msg":"UserFollowing list does not exists"
            })      

#swagger implementation
class CreateFollow(APIView):
    '''
    add following
    '''
    @swagger_auto_schema(
        operation_description="update Following",
        request_body=FollowSerializer,
    )
    def post(self,request):
        data=request.data
        serializer=FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,
                         "data":serializer.data,
                         "message":"follow successfully"} )

        return Response({"data":serializer.errors,"msg":"you already followed this user"})


class GetFollow(APIView):
    '''
    get userFollowing by PK
    '''
    @csrf_exempt
    def get_object(self,pk):
        try:
            return UserFollowing.objects.get(pk=pk)
        except UserFollowing.DoesNotExist:
            return ResponseNotFound()

    def post(self,request,pk):
        try:
            follow=self.get_object(pk)
            serializer=FollowSerializer(follow)
            return ResponseOk({"data":serializer.data,
                                "status":status.HTTP_200_OK,
                                "message":"get Userfollow by pk"})
        except:
            return  ResponseBadRequest(
                {
                    "data":None,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Comment Does Not exists."
                }
            )    

class UpdateFollow(APIView):
    '''
    Update UserFollowing 
    '''

    def get_object(self,pk):
        try:
            return UserFollowing.objects.get(pk=pk)
        except UserFollowing.DoesNotExist:
            return ResponseNotFound()
    
    @swagger_auto_schema(
        operation_description="update Following",
        request_body=FollowSerializer,
    )        

    @csrf_exempt
    def update(self,request,pk):
        try:
            data=request.data        
            follow=self.get_object(pk)
            serializer=FollowSerializer(follow)   
            if serializer.is_valid():
                serializer.save()
                return ResponseOk({"data":serializer.data,
                                    "status":status.HTTP_200_OK,
                                    "message":"update UserFollowing successfully"}) 
        except:
            return ResponseBadRequest({"data":None,
                                        "status":status.HTTP_400_BAD_REQUEST,
                                        "message":"UserFollowing does not exists."})   


class DeleteFollow(APIView):
    '''
    delet UserFollowing
    '''

    def get_object(self,pk):
        try:
            return UserFollowing.objects.get(pk=pk)
        except UserFollowing.DoesNotExist:
            return ResponseNotFound()

    @csrf_exempt
    def delete(self,request,pk):
        try:
            follow=self.get_object(pk)
            follow.delete()
            return ResponseOk({"data":None,
                                "status":status.HTTP_200_OK,
                                "message":"UserFollowing deleted successfully"})

        except:
            return ResponseBadRequest({"data":None,
                                        "status":status.HTTP_400_BAD_REQUEST,
                                        "message":"UserFollowing does not exists"})                        


        # UserFollowing.objects.create(profile_id=data.get('profile_id'),following_user_id=data.get('following_user_id'))


class PostCreateGen(generics.GenericAPIView):
    def post(self,request):
        post=Post.objects.all().values()

        # dictV=dict()
        # dictV['data']=post
        # dictV['msg']="list All posts"
        return Response({'data':post,'msg':'All Matches','status':'200'})


# Rajesh Sir API.
class UpdateNotification(generics.GenericAPIView):
    def post(self,request):
        data=request.data
        n=UserNotifications.objects.filter(User_id=request.data.get('User_id'))
        n.update(text=request.data.get('text'))
        return Response({
          "data":{"Notifications": n.values()},
          "msg":'Notifications Updated successfully.',
          "status":200
        })

        # serializer=UserNotificationsSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()

        #     return Response({"data":data,
        #                      "status":status.HTTP_200_OK,
        #                      "message":"notification create successfully"})

        # return ResponseBadRequest({"data":None,
        #                             "status":status.HTTP_400_BAD_REQUEST,
        #                             "message":"notification does not create"})


# class CommentSettings(generics.GenericAPIView):
#     def post(self,request):
#         data=request.data
        
#         # c=CommentSettings.objects.filter(User_id=data.get('User_id'))
#         # c.update(status=data.get('status'))  
#         serializer=CommentSettingsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data":serializer.data})
#         return Response({"data":None})    

#         # CommentSettings.objects.filter(User_id=request.data.get('User_id')).update(status=Fasle)

class CommentSettingsAPI(generics.GenericAPIView):
    def post(self,request):
       data=request.data
       u=User.objects.filter(id=data.get('User_id'))
       if u:
          u=User.objects.get(id=data.get('User_id'))
          if len(CommentSettings.objects.filter(User_id=u))>0:
             CommentSettings.objects.update(User_id=u,Status=data.get('Status'))
             return Response({"data":"CommentSettings updated successfully"})
          else:
             c=CommentSettings.objects.create(User_id=u,Status=data.get('Status'))
             c.save()
             return Response({"data":"CommentSettings created successfully"})
       else:
           return Response({"msg":"User does not exists"})        
    


class LikeSettingsAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
       data=request.data
       u=User.objects.filter(id=data.get('User_id'))      
       if u:
           u=User.objects.get(id=data.get('User_id'))
           if len(LikeSettings.objects.filter(User_id=u))>0:
               LikeSettings.objects.update(User_id=u,Status=data.get('Status'))
               return Response({"data":"LikeSettings updated successfully"})
           else:
               l=LikeSettings.objects.create(User_id=u,Status=data.get('Status'))
               l.save()
               return Response({"data":"LikeSettings created successfully"})
       else:
           return Response({"msg":"User with this id does not exists"})        


class ShareSettingsAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
       data=request.data
       u=User.objects.filter(id=data.get('User_id'))
       print(u)
       if u:
            u=User.objects.get(id=data.get('User_id'))
            print(u)
            if len(ShareSettings.objects.filter(User_id=u))>0:
               ShareSettings.objects.update(User_id=u,Status=data.get('Status'))
               return Response({"msg":"ShareSettings updated successfully"})  
            else:
               s=ShareSettings.objects.create(User_id=u,Status=data.get('Status'))  
               s.save()
               return Response({"msg":"ShareSettings created successfully"})
       else:
           return Response({"msg":"User with this id does not exists"})      

# class CommentSettingsAPI(generics.GenericAPIView):
#     # permission_classes = (IsAuthenticated,)
#     def post(self, request, *args, **kwargs):
#         n=CommentSettings.objects.filter(User_id=request.POST['User_id'])
#         print(n)
#         n.update(Status=request.POST['Status'])
#         return Response({
#         "data":{"Notifications": n.values('Status','User_id')[0:]},
#         "msg":'Notifications Updated successfully.',
#         "status":200
#         })





def index(request):
    return render(request, 'app/index.html')


def room(request, room_name):
        return render(request, 'chat/room.html', {
        'room_name': room_name
})