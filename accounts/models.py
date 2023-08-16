from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

# Create your models here.


ROLE_CHOICES = (
    ('admin', 'admin'),
    ('simple_user', 'simple user'),
)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='user-images/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.role == 'admin':
            return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.role == 'admin':
            return True

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
