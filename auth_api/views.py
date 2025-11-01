from rest_framework import serializers, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from core.status import *

# -------------------------------
# 🔹 Serializers
# -------------------------------
class JWTLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class JWTLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs


# -------------------------------
# 🔹 Login View
# -------------------------------
class JWTLoginView(generics.GenericAPIView):
    serializer_class = JWTLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=S401)
        if not user.is_active:
            return Response({"error": "Account is not active"}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"username": user.username, "email": user.email},
            },
            status=S200,
        )

class JWTRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
# -------------------------------
# 🔹 Logout View
# -------------------------------
class JWTLogoutView(generics.GenericAPIView):
    serializer_class = JWTLogoutSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=S200)
        except Exception:
            return Response({"error": "Invalid token"}, status=S400)
