# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from user import views

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name="signup"),
    path('signin/',views.SigninView.as_view(),name="signin"),

    path("profile/api/v1/create/", views.CreateProfile.as_view(), name="createprofile"),
    path("profile/api/v1/list/", views.GetAllProfile.as_view(), name="getallprofile"),
    path("profile/api/v1/get/<int:pk>/", views.GetProfile.as_view(), name="getprofile"),
    path("profile/api/v1/update/<int:pk>/", views.UpdateProfile.as_view(), name="updateprofile"),
    path("profile/api/v1/delete/<int:pk>/", views.DeleteProfile.as_view()),

    path("category/api/v1/create/", views.CreateCategory.as_view(), name="category"),
    path("category/api/v1/list/", views.GetAllCategory.as_view(), name="category"),
    path("category/api/v1/get/<int:pk>/", views.GetCategory.as_view(), name="category"),
    path("category/api/v1/update/<int:pk>/", views.UpdateCategory.as_view(), name="category"),
    path("category/api/v1/delete/<int:pk>/", views.DeleteCategory.as_view()),

    path("post/api/v1/create/", views.CreatePost.as_view(), name="post"),
    path("post/api/v1/list/", views.GetAllPost.as_view(), name="post"),
    path("post/api/v1/get/<int:pk>/", views.GetPost.as_view(), name="post"),
    path("post/api/v1/update/<int:pk>/", views.UpdatePost.as_view(), name="post"),
    path("post/api/v1/delete/<int:pk>/", views.DeletePost.as_view()),

    path("comment/api/v1/create/", views.CreateComment.as_view(), name="comment"),
    path("comment/api/v1/list/", views.GetAllComment.as_view(), name="comment"),
    path("comment/api/v1/get/<int:pk>/", views.GetComment.as_view(), name="comment"),
    path("comment/api/v1/update/<int:pk>/", views.UpdateComment.as_view(), name="comment"),
    path("comment/api/v1/delete/<int:pk>/", views.DeleteComment.as_view()),

    path("reply/api/v1/create/", views.CreateReply.as_view(), name="createreply"),
    path("reply/api/v1/list/", views.GetAllReply.as_view(), name="replylist"),
    
    path("allpost", views.PostCreateGen.as_view()),
    path("addfollower", views.AddFollowing.as_view()),

    path("follow/api/v1/create/", views.CreateFollow.as_view()),
    path("follow/api/v1/list/", views.GetAllFollow.as_view(), name="comment"),
    path("follow/api/v1/get/<int:pk>/", views.GetFollow.as_view(), name="comment"),
    path("follow/api/v1/update/<int:pk>/", views.UpdateFollow.as_view(), name="comment"),
    path("follow/api/v1/delete/<int:pk>/", views.DeleteFollow.as_view()),


    path("notification/api/v1/create/", views.UpdateNotification.as_view()),

    path("commentsetting/", views.CommentSettingsAPI.as_view()),
    path("LikeSetting/", views.LikeSettingsAPI.as_view()),
    path("ShareSetting/", views.ShareSettingsAPI.as_view()),

    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),



    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]