from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from src.users.models import CustomUser


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password', 'phone', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = CustomUser.objects.create_user(email=validated_data['email'],
                                                  password=validated_data['password'],
                                                  name=validated_data['name'],
                                                  phone=validated_data['phone'],
                                                  user_type=validated_data['user_type']
                                                  )
            user.save()
            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone', 'user_type')
