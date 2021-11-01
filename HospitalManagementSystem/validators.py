from django.core.validators import RegexValidator


def only_alpha_numeric_space_validator(message=None, code=None,):
    msg = message or "This field should only contains alphanumeric and space"
    return RegexValidator(r'[\w\s\d]+', message=msg, code=code)
