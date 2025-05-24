import random
from .models import User
from datetime import datetime
from django.http import Http404
from .permissions import IsAdmin
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from server.settings.base import DEFAULT_FROM_EMAIL
from django.contrib.auth import password_validation
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import SignUpSerializer, LoginSerializer, UserSerializer
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

import json

def send_otp_email(request, email):  
    otp = random.randint(100000, 999999)
    otp_created_at = timezone.now()

    otp_created_at_str = otp_created_at.isoformat()

    # Store the OTP and datetime string in the session
    request.session["reset_otp"] = otp
    request.session["otp_created_at"] = otp_created_at_str
    request.session["user_email"] = email

    mail = send_mail(
        'Forgot Password OTP',
        f'Your OTP to reset your password is {otp}. Please use this code to complete the process.',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
    if not mail:
        return otp  

    return otp


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role
            }
            return Response(
                {
                    "message": "Registration successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            refresh = RefreshToken.for_user(user)
            user_data = {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "username": user.username,
            }



            return Response(
                {
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RequestPasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'message': 'No account with this email exists'}, status=status.HTTP_404_NOT_FOUND)

        otp = send_otp_email(request, email)
        print("Generated OTP:", otp)
        cache.set(f'reset_otp_{email}', otp, timeout=300)
        return Response({
            'message': 'OTP sent successfully',
            'email': email 
        }, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not email or not otp:
            return Response(
                {'message': 'Both email and OTP are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        stored_otp = cache.get(f'reset_otp_{email}')
        print(f"Stored OTP for {email}:", stored_otp)
        print("Submitted OTP:", otp)

        if stored_otp is None:
            return Response(
                {'message': 'OTP expired or invalid request'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if str(stored_otp) == str(otp):
            cache.set(f'otp_verified_{email}', True, timeout=300)
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


        
class ResetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new-password')
        
        if not email or not new_password:
            return Response(
                {'message': 'Both email and new password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not cache.get(f'otp_verified_{email}'):
            return Response(
                {'message': 'OTP verification required before password reset'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {'message': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            password_validation.validate_password(new_password, user)
            user.set_password(new_password)
            user.save()
            
            # Clean up cache entries
            cache.delete(f'reset_otp_{email}')
            cache.delete(f'otp_verified_{email}')
            
            return Response(
                {'message': 'Password reset successfully!'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )