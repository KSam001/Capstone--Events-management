from rest_framework import serializers
from .models import CustomUser

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        # Include all necessary fields for registration
        fields = ('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'password')

    def create(self, validated_data):
        """Creates and returns a new user."""
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password']
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for reading/updating user profile data."""
    class Meta:
        model = CustomUser
        # Exclude sensitive fields like password
        fields = ('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'is_staff')
        read_only_fields = ('email', 'is_staff')
