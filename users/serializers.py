# users/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError
from users.models import User, Profile, PhoneNumber
from users.validations import UserDataValidator


# ------------------------------------------------
# ✅ Profile Serializer
# ------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'full_name', 'profile_image', 'job_title',
            'bio', 'date_of_birth', 'gender', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ------------------------------------------------
# ✅ Phone Number Serializer (uses validator)
# ------------------------------------------------
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = [
            'id', 'country_code', 'number', 'type', 'verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        number = data.get('number')
        country_code = data.get('country_code')

        # use the validator class
        try:
            UserDataValidator.validate_phone(number, country_code)
        except ValidationError as e:
            raise serializers.ValidationError({'number': e.messages})

        return data


# ------------------------------------------------
# ✅ User Serializer (for registration / profile)
# ------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password2',
            'country', 'city', 'postal_code', 'address',
            'is_active', 'phone_numbers', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # ---------------------------------------------
    # ✅ Field-level and object-level validation
    # ---------------------------------------------
    def validate(self, data):
        # 1. password match check
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})

        # 2. use central validator
        try:
            UserDataValidator.validate_username(data.get('username'))
            UserDataValidator.validate_password(data.get('password'), data.get('username'))
            UserDataValidator.validate_email(data.get('email'))
            UserDataValidator.validate_country_city(data.get('country'), data.get('city'))
        except ValidationError as e:
            # automatically wrap messages for DRF
            raise serializers.ValidationError({'detail': e.messages})

        return data

    # ---------------------------------------------
    # ✅ Create method (hash password properly)
    # ---------------------------------------------
    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hashes the password
        user.save()
        return user
