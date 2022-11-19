from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# from main.models import Basket


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)

        # user.basket = Basket.objects.create()
        user.save()
        return user

    
    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save()
        return user



class User(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    # basket = models.OneToOneField(Basket, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
