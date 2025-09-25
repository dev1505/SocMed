from django.db import models
from SocialMediaApp.models import User


class UserMessages(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="from_user",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="to_user",
    )
    message = models.CharField(
        max_length=250,
        blank=False,
        null=False,
    )
    date = models.DateField(auto_now_add=True, blank=False)
    message_time = models.TimeField(auto_now_add=True, blank=False)
