from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from accounts.serializers import UserSerializer, LoginSerializer


class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(**serializer.data)

        if user:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({"token": token.key})

        return Response(
            {"error": "user not found"}, status=status.HTTP_401_UNAUTHORIZED
        )
