import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"


def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid


def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False