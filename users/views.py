# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from users.models import User,Profile
from users.serializers import UserSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "User created successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )
class UserUpdateViews(generics.RetrieveUpdateAPIView):
    queryset  = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer()
        serializer.save()
        return Response(
            {"message": "User updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Temporary test version:
    Uses the first user in DB for testing (no authentication yet).
    """
    serializer_class = ProfileSerializer  # ✅ correct name

    def get_object(self):
        # Get first user (for testing only)
        user = User.objects.first()
        if not user:
            raise ValueError("No users exist in database yet.")

        # Get or create profile for that user
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "profile": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)