from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, fullname, password):
        if not phone_number:
            raise ValueError('phone number required')
        if not email:
            raise ValueError('email required')
        if not fullname:
            raise ValueError('fullname required')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, fullname, password):
        user = self.create_user(phone_number, email, fullname, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        