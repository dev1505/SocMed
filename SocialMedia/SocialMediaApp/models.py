from django.db import models


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):  # type: ignore
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])


class User(SoftDeleteModel):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True, null=True)
    email = models.EmailField(max_length=150, blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        Followers.objects.filter(
            models.Q(follower=self.pk) | models.Q(following=self.pk)
        ).delete()
        self.save(update_fields=["is_deleted"])


class Credentials(models.Model):
    auth_id = models.CharField(max_length=150, blank=True, unique=True)
    password = models.CharField(max_length=150, blank=True, null=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    auth_id_by = models.CharField(max_length=255, blank=True)


class Followers(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="follower",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="following",
    )
    following_time = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )

    class Meta:
        unique_together = ("follower", "following")
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(follower=models.F("following")),
                name="prevent_self_follow",
            )
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
