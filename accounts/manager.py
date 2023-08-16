from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password):
        if not email:
            raise ValueError('email must be set')
        if not first_name:
            raise ValueError('first name must be set')
        if not last_name:
            raise ValueError('last name must be set')

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        user.role = 'admin'
        user.is_active = True
        user.save(using=self._db)
        return user
