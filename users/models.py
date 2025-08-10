from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class MyUserManager(BaseUserManager):
  def create_superuser(self, email, password):
    user = self.model(email=email)
    user.set_password(password)
    user.is_superuser = True
    user.is_active = True
    user.is_staff = True
    user.save(using=self._db)
    return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True,
                              max_length=255, blank=True, null=True)
    username = models.CharField(
        "User Name", unique=True, max_length=255, blank=True, null=True)
    first_name = models.CharField(
        "First Name", max_length=255, blank=True, null=True)
    last_name = models.CharField(
        "Last Name", max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(
        "Profile Picture", upload_to="profile_pictures/", blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_locked = models.BooleanField(
        'Locked', default=False, blank=True, null=True)
    is_active = models.BooleanField(
        'Active', default=True, blank=True, null=True)
    is_staff = models.BooleanField('Staff', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
      return self.email