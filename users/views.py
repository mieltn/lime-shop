from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"msg": "admin access is required for this action"}
            )
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
