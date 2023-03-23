from os import access
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email,  first_name, last_name,contact_no,address, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            contact_no=contact_no,
            address=address,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  first_name, last_name,contact_no,address, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            contact_no=contact_no,
            address=address,
        )
        user.is_admin = True
        user.is_verified = True
        user.save(using=self._db)
        return user

# Custom User Model


class User_data(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    date_of_birth = models.DateField(null=True)
    upload_image = models.ImageField(upload_to ='image_uploads/',null=True)
    upload_id_proof = models.FileField(upload_to ='ID_proof_uploads/',null=True)
    contact_no = models.CharField(max_length=12,null=True)
    address = models.CharField(max_length=25,null=True)
    work_exp = models.CharField(max_length=12 ,null=True)
    Roles = [
        ("manager", "manager"),
        ("account", "account"),
        ("Customer", "Customer"),
        ("Packer", "Packer"),
        ("Farm laborer", "Farm laborer"),
        ("Gardener", "Gardener"),
        ("Production worker", "Production worker"),
        ("Forklift operator", "Forklift operator"),
        ("Landscape technician", "Landscape technician"),
        ("Package handler", "Package handler"),
    ]
    work_field = models.CharField(max_length=50, choices=Roles,null=True)
    access_token = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'contact_no','address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

