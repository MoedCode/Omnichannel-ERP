in those endpoint there are no way tp provide  request haders wither with from or row data
```py
# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from users.models import User,Profile
from users.serializers import UserSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

@permission_classes([AllowAny])
class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "User created successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )
class UserUpdateViews(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always update the currently authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Use the authenticated user instead of first()
        user = self.request.user
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Profile updated successfully.",
            "profile": serializer.data
        }, status=status.HTTP_200_OK)
```