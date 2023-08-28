from django.contrib.auth import login
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from account.models import User
from account.serializers import RegisterSerializer, UserSerializer, LoginSerializer


class RegisterAPIView(generics.GenericAPIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
        })



class LoginAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        data = UserSerializer(user).data
        return Response({'user': data}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = RegisterSerializer(user)
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = RegisterSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)