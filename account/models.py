from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager as DefaultUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from HospitalManagementSystem.validators import only_alpha_numeric_space_validator

from HospitalManagementSystem.utilities import unique_slug_generate


class GenderChoices(models.TextChoices):
    MALE = ("m", "Male")
    FEMALE = ("f", "Female")
    TRANSGENDER = ("t", "Transgender")
    OTHER = ("o", "Other")


class UserManager(DefaultUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password,):
        usr = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email
        )

        usr.set_password(password)
        usr.save()
        return usr

    def create_superuser(self, first_name, last_name, email, password, phone_number):
        usr = self.create_user(first_name, last_name, phone_number=phone_number, password=password, email=email)
        usr.is_superuser = True
        usr.save()
        return usr

    def search(self, query):
        qry = models.Q(first_name__icontains=query) | models.Q(last_name__icontains=query)
        return self.filter(qry)


def upload_user_to_path(instance, filename):
    import os
    unique = instance.id or instance.username
    new_filename = str(unique) + os.path.splitext(filename)[-1]
    return os.path.join("user", "profile_picture", new_filename)


class User(PermissionsMixin, AbstractBaseUser):
    first_name = models.CharField(max_length=60, validators=[only_alpha_numeric_space_validator()])
    last_name = models.CharField(max_length=120, validators=[only_alpha_numeric_space_validator()])
    gender = models.CharField(max_length=30, choices=GenderChoices.choices, null=True, blank=True)
    dob = models.DateField(verbose_name='Date of birth', null=True)
    email = models.EmailField(unique=True,)
    phone_number = PhoneNumberField(unique=True)
    picture = models.ImageField(null=True, blank=True, upload_to=upload_user_to_path)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    session_key = models.CharField(max_length=32, unique=True, null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    USERNAME_FIELD = 'phone_number'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    class Meta:
        """Meta definition for User."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ("first_name", "last_name", "email")

    def __str__(self):
        """Unicode representation of User."""
        return self.get_full_name()

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def get_name_abr(self):
        f_abr = "".join([list(n)[0] for n in self.first_name.split(" ")]).upper()
        l_abr = "".join([list(n)[0] for n in self.last_name.split(" ")]).upper()
        return f_abr + l_abr

    @property
    def is_staff(self):
        return self.is_active and (self.is_superuser or self.is_admin)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        if self.is_superuser or self.is_admin:
            return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return self.is_staff


@receiver(models.signals.pre_save, sender=User)
def auto_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generate(instance)
