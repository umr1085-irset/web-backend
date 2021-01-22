from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.views import APIView
import requests

from .serializers import UserSerializer, MyTokenObtainPairSerializer, GetFullUserSerializer, GetFullUserProfilSerializer

User = get_user_model()


@api_view(['GET'])
def get_current_user(request):
    serializer = GetFullUserProfilSerializer(request.user)
    return Response(serializer.data)

@permission_classes([permissions.AllowAny])
class UserActivationView(APIView):
    def get(self, request, uid, token, format = None):
        payload = {'uid': uid, 'token': token}
        url = "http://localhost:8000/api/v1/auth/users/activation/"
        response = requests.post(url, data = payload)
        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = GetFullUserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = GetFullUserProfilSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Restriction view
class HelloWorldView(APIView):
    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)