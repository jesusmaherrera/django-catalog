"""Users serializers."""

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator
from django.conf import settings

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# models
from apps.users.models import User, Profile

# Tasks
from apps.taskapp.tasks import send_confirmation_email

# Serializers
# from apps.users.serializers import ProfileModelSerializer

# utilities
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """user model serializer."""

    # profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            # 'profile',
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials.')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def save(self):
        """generate or retreive a new token."""

        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AcountVerificationSerializer(serializers.Serializer):
    """Acount verification serializer."""
    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(
                data, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token.')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token.')
        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verification status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()


class UserSignUpSerializer(serializers.Serializer):
    """User signup serializer.

    Handle the signup data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        min_length=4, max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=(
            "Phone number must be entered in the format:"
            " +999999999. Up to 15 digits allowed."
        )
    )
    phone_number = serializers.CharField(
        validators=[phone_regex, ], max_length=17)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify ásswords match."""
        password = data['password']
        password_confirmation = data['password']
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(
            is_verified=False, is_client=True, **data)
        Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk)
        return user
