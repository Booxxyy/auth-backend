import bcrypt
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        raw_password = validated_data.pop('password')

        password_hash = bcrypt.hashpw(
            raw_password.encode('utf-8'),
            bcrypt.gensalt()
        )
        user = User.objects.create(
            password = password_hash.decode('utf-8'),
            **validated_data
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('Неверный email или пароль')

        if not bcrypt.checkpw(
            data['password'].encode('utf-8'),
            user.password.encode('utf-8')
        ):
            raise serializers.ValidationError('Неверный email или пароль')

        data['user'] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'role_name', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'is_active', 'created_at')

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance