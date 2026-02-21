import datetime
import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, UpdateProfileSerializer
from users.models import User

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': f'Пользователь {user.email} создан'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({'token': token}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        return Response(
            {'message': 'Вы вышли из системы'},
            status=status.HTTP_200_OK
        )

class ProfileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        if not isinstance(request.user, User):
            return Response({'detail': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not isinstance(request.user, User):
            return Response({'detail': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {'message': 'Аккаунт удалён. Вы вышли из системы'},
            status=status.HTTP_200_OK
        )
