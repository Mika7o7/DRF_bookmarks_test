from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# hook in the New Manager to our Model
class User(AbstractUser):  # from step 2
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = None
  
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()
    

    def __str__(self):
        return self.email
    

    # Add unique related_name attributes to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        related_query_name='customuser_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',
        related_query_name='customuser_user_permission',
    )



class Bookmark(models.Model):
    TYPE_CHOICES = [
        ('website', 'Website'),
        ('book', 'Book'),
        ('article', 'Article'),
        ('music', 'Music'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()
    type = models.CharField(
                            max_length=20,
                            choices=TYPE_CHOICES,
                            default='website',
                            )
    image_preview = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
                                    "Collection",
                                    on_delete=models.SET_NULL,
                                    related_name="bookmarks",
                                    blank=True,
                                    null=True,
                                )

    def __str__(self):
        return self.title



class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
    
