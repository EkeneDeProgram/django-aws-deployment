# Related third-party imports
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

# Local application/library-specific imports
from .models import Process


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is responsible for handling the validation and creation of a new user.
    It ensures that the password is handled securely (write-only) and that only necessary
    fields (username, email, password) are included in the request and response.
    """

    # Password field should only be included when writing (i.e., creating a new user)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Fields to be serialized; excluding password field from the response
        fields = ["username", "email", "password"]

    def validate_password(self, value):
        # Use Django's built-in password validation
        validate_password(value)
        return value

    def create(self, validated_data):
        # Create a new user using the validated data and hash the password securely
        user = User.objects.create_user(**validated_data)
        return user


class ProcessSerializer(serializers.ModelSerializer):
    """
    Serializer for the Process model.

    This serializer is used to validate and serialize the data for the `Process` model.
    It specifies which fields will be included when creating, updating, or retrieving instances
    of the `Process` model. The specified fields are `id`, `email`, and `message`.
    """

    class Meta:
        model = Process  # Specify the Django model
        fields = ["id", "email", "message"]  # Specify the fields to serialize
