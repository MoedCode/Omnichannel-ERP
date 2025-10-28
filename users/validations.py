#users/validations.py
import re
from django.core.exceptions import ValidationError
from django_countries import countries
from phonenumbers import parse as parse_phone, is_valid_number, NumberParseException
import phonenumbers
import pycountry


class UserDataValidator:
    """
    Centralized validation class for user-related data:
    username, password, email, country, city, and phone number.
    """

    # 1️⃣ Validate Username
    @classmethod
    def validate_username(cls, username):
        if not username:
            raise ValidationError("Username must be provided.")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            return ValidationError("Username cannot contain spaces or special characters.")

        return username

    # 2️⃣ Validate Password
    @classmethod
    def validate_password(cls, password, username=None):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        if username and username.lower() in password.lower():
            raise ValidationError("Password should not contain your username.")
        return password

    # 3️⃣ Validate Email
    @classmethod
    def validate_email(cls, email):
        if not email:
            return None  # Optional

        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format.")

        allowed_domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'icloud.com']
        domain = email.split('@')[-1].lower()
        if not any(domain.endswith(d) for d in allowed_domains):
            raise ValidationError("Email domain is not recognized as a valid provider.")
        return email

    # 4️⃣ Validate Country and City
    @classmethod
    def validate_country_city(cls, country_name, city_name):
        if not country_name:
            return None, None

        try:
            country = pycountry.countries.lookup(country_name)
        except LookupError:
            raise ValidationError(f"Invalid country name: {country_name}")

        # Optional: Check city exists using pycountry or simpledb
        if city_name:
            city_name = city_name.strip().title()
            # Placeholder for real API/database check
            if len(city_name) < 2:
                raise ValidationError("City name is too short to be valid.")

        return country.alpha_2, city_name

    # 5️⃣ Validate Phone Number
    @classmethod
    def validate_phone(cls, phone_number, country_code=None):
        if not phone_number:
            raise ValidationError("Phone number is required.")

        try:
            if country_code:
                parsed = parse_phone(phone_number, country_code)
            else:
                parsed = parse_phone(phone_number, None)
        except NumberParseException:
            raise ValidationError("Invalid phone number format.")

        if not is_valid_number(parsed):
            raise ValidationError("Invalid phone number for the specified country.")

        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
