from django.db import models


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):  # type: ignore
        """
        Instead of deleting the object, mark it as deleted.
        """
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        """
        To 'undo' the soft deletion if needed.
        """
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
        return True


class Credentials(models.Model):
    auth_id = models.CharField(max_length=150, blank=True, unique=True)
    password = models.CharField(max_length=150, blank=True, null=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    auth_id_by = models.CharField(max_length=255, blank=True)
