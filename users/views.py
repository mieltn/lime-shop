from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer
from limeshop.permissions import IsAuthOrCreate


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthOrCreate]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({'loggedOut': True}, status=status.HTTP_200_OK)
