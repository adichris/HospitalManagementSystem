from django.db import models
from django_countries.fields import CountryField
from account.models import User


class Address(models.Model):
    country = CountryField()
    region = models.CharField(max_length=120, help_text="The country region or state")
    city = models.CharField(max_length=120, null=True, help_text="The city, community or town your live in.")
    house_number = models.CharField(max_length=120, null=True, blank=True,
                                    help_text="Your house number.")
    profile = models.ForeignKey(User, on_delete=models.CASCADE, )

    class Meta:
        unique_together = ("profile", "id")

    def __str__(self) -> str:
        return self.city + ", " + self.house_number
