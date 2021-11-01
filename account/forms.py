from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import MinimumLengthValidator


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
        fields, plus a repeated password."""
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "dob", "gender", "phone_number",
        )

    def clean_password_confirmation(self):
        pwd = self.cleaned_data.get("password")
        pwd_cfm = self.cleaned_data.get("password_confirmation")

        minimum_password_validator = MinimumLengthValidator(4)
        minimum_password_validator.validate(pwd_cfm)

        if pwd != pwd_cfm:
            raise forms.ValidationError("passwords does not match", code="invalid")

        return pwd_cfm

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "gender", "dob", "email", "phone_number", "picture", "is_active", "is_admin",
            "is_superuser"
        )
