from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import RegexValidator

from django_countries.fields import CountryField



class UserProfile(models.Model):
    """
    Extends base User model.
    Allows saving shipping details and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_full_name = models.CharField(max_length=100, null=True, blank=True)
    saved_email = models.EmailField(max_length=300, null=True, blank=True)
    saved_phone_number = models.CharField(
        max_length=16, blank=True, null=True, validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+123456789'.\
                     Up to 15 digits allowed.",
            code="invalid")])
    saved_address_line1 = models.CharField(max_length=200, null=True, blank=True)
    saved_address_line2 = models.CharField(max_length=200, null=True, blank=True)
    saved_region = models.CharField(max_length=85, null=True, blank=True)
    saved_city = models.CharField(max_length=85, null=True, blank=True)
    saved_postcode = models.CharField(max_length=30, null=True,
        blank=True, validators=[RegexValidator(
            regex=r'^[\d\-a-zA-Z]+$', 
            message="Only letters, numbers and hyphens allowed.",
            code="invalid")])
    saved_country = CountryField(blank_label="Country *", null=True, blank=True)

    def __str__(self):
        if self.user:
            return self.user.email


@receiver(pre_save, sender=User)
def use_email_as_username(sender, instance, **kwargs):
    user_email = instance.email
    username = user_email[:30]
    n = 1
    while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        n += 1
        username = user_email[:(29 - len(str(n)))] + '-' + str(n)
    instance.username = username

@receiver(post_save, sender=User)
def user_profile_create_update(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Only save profile details if the profile exists
    instance.userprofile.save()
