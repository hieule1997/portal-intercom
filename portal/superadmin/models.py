from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django_cryptography.fields import encrypt

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, fullname, key, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            fullname=fullname,
            key=key,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, fullname, key, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            fullname=fullname,
            key=key,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_adminkvm = models.BooleanField(default=False)
    token_id = models.CharField(max_length=255, null=True)
    token_expired = models.DateTimeField(null=True)
    money=models.CharField(max_length=100, default="0")

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def check_expired(self):
        time = self.token_expired - timezone.datetime.now(timezone.utc)
        return time > timezone.timedelta(seconds=0)
class Server(models.Model):
    project = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    host = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    ip = models.CharField(max_length=255,null=True)
    ram = models.IntegerField()
    vcpus = models.IntegerField()
    disk = models.IntegerField()
    owner = models.ForeignKey('Myuser', models.CASCADE)
    created = models.CharField(max_length=255, null=True)
    i_d = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'serverVM'

class Sshkeys(models.Model):
    ops = models.ForeignKey('Ops', models.CASCADE)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('Myuser', models.CASCADE)

    class Meta:
        db_table = 'sshkeys'

class Images(models.Model):
    ops = models.ForeignKey('Ops', models.CASCADE)
    name = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    i_d = models.CharField(max_length=255)

    class Meta:
        db_table = 'images'

class Snapshot(models.Model):
    ops = models.ForeignKey('Ops', models.CASCADE)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('Myuser', models.CASCADE)
    i_d = models.CharField(max_length=255)

    class Meta:
        db_table = 'snapshot'

class Networks(models.Model):
    owner = models.ForeignKey('Myuser', models.CASCADE)
    name = models.CharField(max_length=255)
    subnets_associated = models.CharField(max_length=255)
    shared = models.IntegerField()
    external = models.IntegerField()
    status = models.CharField(max_length=100)
    admin_state_up = models.IntegerField()


    class Meta:
        db_table = 'client_networks'

class Oders(models.Model):
    service = models.CharField(max_length=255)
    server = models.CharField(max_length=255)
    ip = models.CharField(max_length=255,null=True)
    price = models.CharField(max_length=255)
    status = models.IntegerField(default=1)
    owner = models.ForeignKey('Myuser', models.CASCADE)
    created = models.DateTimeField()

    class Meta:
        db_table = 'oders'
        
class Ops(models.Model):
    name = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = encrypt(models.CharField(max_length=50))
    project = models.CharField(max_length=255)
    userdomain = models.CharField(max_length=255)
    projectdomain = models.CharField(max_length=255)

    class Meta:
        db_table = 'ops'