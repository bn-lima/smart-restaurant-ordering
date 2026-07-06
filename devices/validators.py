from django.core.validators import RegexValidator

PASSWORD_VALIDATOR = RegexValidator( # Validador de senha (mínimo 8 caracteres sem espaços)
    regex=r"^\S{8,}$",
    message="Password must contain at least 8 characters and cannot contain spaces"
)