from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserRegistrationSerializer, CustomUserSerializer
from .models import CustomUser

class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = (permissions.AllowAny,) # Allow anyone to register

class ProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint for viewing and updating the user's own profile."""
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Returns the profile object for the currently authenticated user."""
        return self.request.user
