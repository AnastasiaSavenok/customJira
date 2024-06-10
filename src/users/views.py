from django.contrib.auth import login, logout
from rest_framework import status, mixins, views
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from src.users.models import CustomUser
from src.users.permissions import IsCustomer
from src.users.serializers import LoginSerializer, RegisterSerializer, UserSerializer, UserDetailSerializer


class RegisterAPIView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = RegisterSerializer
    get_queryset = CustomUser.objects.all

    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email=request.data.get('email'))
            if user:
                return Response({'Email is already used'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            if user:
                user.set_password(user.password)
                user.save()
                return Response({"Registration success":
                                     UserSerializer(user, context=self.get_serializer_context()).data},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'Registration failed'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(views.APIView):

    def post(self, request):
        logout(request)
        Response().delete_cookie(key="refreshToken")
        return Response({'message': "Logout successful"}, status=status.HTTP_200_OK)


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, CustomUser.objects.get(email=request.data.get('email')))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class EmployeeListView(ListAPIView):
    queryset = CustomUser.objects.filter(user_type='employee')
    serializer_class = UserDetailSerializer
    permission_classes = [IsCustomer]
