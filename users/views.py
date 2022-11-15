from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model, login, logout

from .models import User
from .serializers import UserSerializer


class UserView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'no authorized user found'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        userAuthenticated = authenticate(request, username=username, password=password)

        if userAuthenticated:
            login(request, userAuthenticated)
            return Response({'isAuthenticated': True}, status=status.HTTP_200_OK)

        return Response({'isAuthenticated': False}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUser(APIView):

    def post(self, request):
        logout(request)
        return Response({'loggedOut': True}, status=status.HTTP_200_OK)
