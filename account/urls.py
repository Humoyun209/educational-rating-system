from django.urls import path, re_path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from account import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('profile/<int:pk>/', views.ProfileAPIView.as_view()),

    re_path(r'^auth/', include('djoser.urls.authtoken')),  # JWT
    path('auth/', include('djoser.urls')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Djoser
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
