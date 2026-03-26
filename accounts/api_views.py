from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Profile

# REGISTER API
class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "customer")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile with role (customer or provider)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User created",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": profile.role,
        })


# LOGIN API
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": user.username
            })

        return Response({"error": "Invalid credentials"}, status=400)