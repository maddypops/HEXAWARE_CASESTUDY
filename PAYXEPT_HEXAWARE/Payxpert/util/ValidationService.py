from Payxpert.exception.InvalidInputException import InvalidInputException
import re
from datetime import datetime


class ValidationService:
    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise InvalidInputException("Invalid email format")

    @staticmethod
    def validate_phone_number(phone_number):
        phone_regex = r'^\d{10}$'
        if not re.match(phone_regex, phone_number):
            raise InvalidInputException("Invalid phone number format. Must be 10 digits.")

    @staticmethod
    def validate_date(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise InvalidInputException("Incorrect date format, should be YYYY-MM-DD")

    @staticmethod
    def validate_non_empty(value, field_name):
        if not value or value.strip() == "":
            raise InvalidInputException(f"{field_name} cannot be empty")

    @staticmethod
    def validate_positive_number(value, field_name):
        if value <= 0:
            raise InvalidInputException(f"{field_name} must be a positive number")
