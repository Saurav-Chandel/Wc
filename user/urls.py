# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',SignUpView.as_view(),name="signup"),
    path('signin/',SigninView.as_view(),name="signin")
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]