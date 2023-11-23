from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def is_valid_password(password):
    try:
        validate_password(password)
        error = ""
        validity = True
    except ValidationError as e:
        error = e.messages[0].title()
        validity = False
    return {"error": error, "validity": validity}