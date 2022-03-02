from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.timezone import now
# Create your models here.


class AppUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)


    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        # email=request.data['email']
        extra_fields.setdefault("username", email)
      
        return self._create_user(email, password, **extra_fields)    

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a Super Admin. Not to be used by any API. Only used for django-admin command.
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)

        user = self._create_user(email, password, **extra_fields)
        return user


class User(AbstractUser):
    first_name = models.CharField(
        max_length=200, default=None, null=True, blank=True
    )
    email=models.EmailField(unique=True,null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    manager = AppUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.username    

GENDER_CHOICES = (
    ("male", "male"),
    ("female", "female"),
)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_picture=models.ImageField(upload_to="profile_picture",null=True,blank=True)
    first_name=models.CharField(max_length=100,blank=True,null=True)
    last_name=models.CharField(max_length=100,blank=True,null=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    dob=models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=100,choices=GENDER_CHOICES)
    about_me=models.TextField(null=True,blank=True)
    

    def __str__(self):
        return self.first_name

class Category(models.Model):
    cat_name=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name


class Post(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=255,blank=True,null=True)
    pic=models.ImageField(upload_to="post_pic",blank=True,null=True)
    tags=models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.posted_by.first_name

class Comments(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_comment")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=255,null=True,blank=True)
    like=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.posted_by.first_name  # kiski post p comment hua

class Reply(models.Model):
    # post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comments=models.ForeignKey(Comments,on_delete=models.CASCADE)
    reply=models.CharField(max_length=100,null=True,blank=True)
    

    def __str__(self):
        return self.comments.user.first_name   # kis user ne comment kiya tha particular post mai.. so it is a reply against particular user that is returned.


TOKEN_TYPE_CHOICES = (
    ("verification", "Email Verification"),
    ("pwd_reset", "Password Reset"),
)

class Token(models.Model):
    token = models.CharField(max_length=300)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    token_type = models.CharField(
        max_length=20, choices=TOKEN_TYPE_CHOICES
    )
    created_on = models.DateTimeField(default=now, null=True, blank=True)
    expired_on = models.DateTimeField(default=now, null=True, blank=True)        