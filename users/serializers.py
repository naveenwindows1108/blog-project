from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('INVALID EMAIL OR PASSWORD')
        attrs['user'] = user
        return attrs


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        email = data.get('email')
        if not email.endswith('@gmail.com'):
            raise serializers.ValidationError('use gmail for creation')
        validate_password(password=password)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('user already exists')
        data['email'] = email
        data['password'] = password
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], email=validated_data['email'], password=validated_data['password'])
        return user


class CRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name','last_name']
