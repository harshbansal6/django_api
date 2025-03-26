from django.shortcuts import render
import random
import uuid
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserOTP
from .serializers import (
    UserRegistrationSerializer,
    OTPVerificationSerializer,
    UserLoginSerializer,
    UserSerializer,
)

# Create your views here.
from django.views.generic import TemplateView

# Add this class at the end of the file
class IndexView(TemplateView):
    template_name = 'authentication/index.html'
    
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            UserOTP.objects.create(user=user, otp=otp)
            
            # Send OTP via email
            send_mail(
                'Verify your account',
                f'Your OTP is: {otp}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            
            return Response({
                'message': 'User registered successfully. Please verify your email with the OTP sent.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                user = User.objects.get(email=email)
                user_otp = UserOTP.objects.filter(user=user, otp=otp, is_verified=False).latest('created_at')
                
                # Verify user
                user.is_active = True
                user.save()
                
                # Mark OTP as verified
                user_otp.is_verified = True
                user_otp.save()
                
                return Response({
                    'message': 'Account verified successfully. You can now login.'
                }, status=status.HTTP_200_OK)
            except (User.DoesNotExist, UserOTP.DoesNotExist):
                return Response({
                    'message': 'Invalid email or OTP.'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(username=email, password=password)
            
            if user is not None:
                if not user.is_active:
                    return Response({
                        'message': 'Account not verified. Please verify your email.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                # Generate auth token if not exists
                if not user.auth_token:
                    user.auth_token = uuid.uuid4()
                    user.save()
                
                response = Response({
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
                
                # Set auth_token cookie
                response.set_cookie(
                    key='auth_token',
                    value=str(user.auth_token),
                    httponly=True,
                    secure=True,
                    samesite='Lax'
                )
                
                return response
            else:
                return Response({
                    'message': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Clear auth_token from user
        request.user.auth_token = None
        request.user.save()
        
        response = Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        
        # Delete auth_token cookie
        response.delete_cookie('auth_token')
        
        return response
