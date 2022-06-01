import email
from tabnanny import verbose
from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

'''
when creating new tables or updating tables
python3 manage.py makemigrations
python3 manage.py migrate
'''

# Create your models here.
#required user manager?
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email adress")
        if not username:
            raise ValueError("User must have a username adress")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            email = self.normalize_email(email),
            username=username,
            first_name = first_name,
            last_name = last_name,
            # is_coach = is_coach,
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username=username,
            first_name = first_name,
            last_name = last_name,
            # is_coach = is_coach,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    # UserId =        models.AutoField(primary_key=True)
    email =         models.EmailField(verbose_name="email", max_length=100, unique=True)
    username =      models.CharField(max_length=20, unique=True)
    first_name =    models.CharField(max_length=30)
    last_name =     models.CharField(max_length=60)
    # is_coach =      models.BooleanField(default=True)

    #required
    date_joined =   models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login =    models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin =      models.BooleanField(default=False)
    is_active =     models.BooleanField(default=True)
    is_staff =      models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    #end required

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyUserManager()

    def __str__(self):  # => returns email as identification (usernmae)
        return self.username

    def has_perm(self, perm, obj=None): # => gives permissions to superuser by returning true or false for is_admin
        return self.is_admin

    def has_module_perms(self, app_label):  # => gives permissions for the rest?
        return True

class GroupProject(models.Model):
    name =                      models.CharField(max_length=128)
    description =               models.TextField()
    final_deadline =            models.DateTimeField()

    def __str__(self):
        return self.name

class LearnerProject(models.Model):
    user =                      models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name =                      models.CharField(max_length=128, blank=False, null=False)
    description =               models.TextField(blank=False, null=False)
    database_schema_picture =   models.ImageField(upload_to="images", blank=True, null=True)
    mockup_picture =            models.ImageField(upload_to="images", blank=True, null=True)
    groupProject =              models.ForeignKey(GroupProject, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Groups(models.Model):
    learnerProject =            models.ForeignKey(LearnerProject, on_delete=models.CASCADE, null=True, blank=True)
    groupProject =              models.ForeignKey(GroupProject, on_delete=models.CASCADE, null=True, blank=True)

class UserPerGroup(models.Model):
    groupProject =              models.ForeignKey(GroupProject, on_delete=models.CASCADE, null=True, blank=True)
    user =                      models.ForeignKey(User, on_delete=models.CASCADE)

class WishList(models.Model):
    user =                      models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groupProject =              models.ForeignKey(GroupProject, on_delete=models.CASCADE, null=True, blank=True)
    whishList =                 models.CharField(max_length=128, blank=False, null=False)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_aut_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)