from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import CustomUser, Profile
from .serializers import UserSerializer, ProfileSerializer

class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        oauth_token = request.data.get('oauth_token')
        if oauth_token:
            try:
                idinfo = id_token.verify_oauth2_token(oauth_token, requests.Request())
                email = idinfo['email']
                user, created = CustomUser.objects.get_or_create(email=email)
                if created:
                    user.set_unusable_password()
                    user.save()
                    Profile.objects.create(user=user, number=request.data.get('number'))
            except ValueError:
                return Response({'error': 'Invalid OAuth token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        oauth_token = request.data.get('oauth_token')

        if oauth_token:
            try:
                idinfo = id_token.verify_oauth2_token(oauth_token, requests.Request())
                email = idinfo['email']
                user, created = CustomUser.objects.get_or_create(email=email)
                if created:
                    user.set_unusable_password()
                    user.save()
            except ValueError:
                return Response({'error': 'Invalid OAuth token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)