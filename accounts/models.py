from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,\
     BaseUserManager, AbstractUser

# User Model Manager
class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, is_admin, is_superuser=False):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_admin = is_admin
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, password2=None, is_admin=False):
        return self._create_user(email, password, first_name, last_name, is_admin)

    def create_superuser(self, email, first_name, last_name, password=None):
        self._create_user(email, password, first_name, last_name, is_admin=True, is_superuser=True)

# User Model for Authentication 
class User(AbstractBaseUser, PermissionsMixin):
    # User Types
    class Types(models.TextChoices):
        READER = "READER", "Reader"
        WRITTER = "WRITTER", "Writter"

    # Type Field
    type = models.CharField(max_length=50, choices=Types.choices, default=Types.READER)

    # Personal Details
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    # is account active
    is_active = models.BooleanField(default=True)

    # accounts permissions
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # accounts creation and updation date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

# Types of User Manager
class ReaderManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.READER)
    
class WritterManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.WRITTER)

# Types of User Proxy Model
class Reader(User):
    # Reader base type is User.Types.READER
    base_type = User.Types.READER
    objects = ReaderManager()
    
    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
        return super().save(*args, **kwargs)

class Writter(User):
    # Writer base type is User.Types.WRITER
    base_type = User.Types.WRITTER
    objects = WritterManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
        return super().save(*args, **kwargs)

    @property
    def more(self):
        return self.writtermore

# Writter More Information
class WritterMore(models.Model):
    # RANK TYPE OF WRITTERs
    class RankType(models.IntegerChoices):
        BRONZE = 1
        SILVER = 2
        GOLD = 3
        PLATINUM = 4
        DIAMOND = 5
        HEROIC = 6
        GRAND_MASTER = 7

    user = models.OneToOneField(Writter, on_delete=models.CASCADE)
    experience = models.PositiveSmallIntegerField(default=0)
    rank = models.IntegerField(choices=RankType.choices, default=RankType.BRONZE)
    

    class Meta:
        verbose_name = "Writter Information"

    def __str__(self):
        return self.user.email