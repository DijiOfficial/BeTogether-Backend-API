import email
from tabnanny import verbose
from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

'''
when creating new tables or updating tables
python3 manage.py makemigrations
python3 manage.py migrate
'''

# Create your models here.
#required user manager?
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, is_coach, password=None):
        if not email:
            raise ValueError("User must have an email adress")
        if not first_name:
            raise ValueError("User must have a first name")
        if not email:
            raise ValueError("Users must have a last name")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            is_coach = is_coach,
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    # UserId =        models.AutoField(primary_key=True)
    email =         models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name =    models.CharField(max_length=30)
    last_name =     models.CharField(max_length=60)
    is_coach =      models.BooleanField(default=True)

    #required
    date_joined =   models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login =    models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin =      models.BooleanField(default=False)
    is_active =     models.BooleanField(default=True)
    is_staff =      models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    #end required

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "is_coach"]

    objects = MyUserManager()

    #don't know what this does
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class LearnerProject(models.Model):
    user =                      models.ForeignKey(User, on_delete=models.CASCADE)
    name =                      models.CharField(max_length=128)
    description =               models.TextField()
    # database_schema_picture =   models.ImageField(upload_to="images", blank=True, null=True)
    # mockup_picture =            models.ImageField(upload_to="images", blank=True, null=True)