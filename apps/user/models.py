from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def full_name(self):
        name = ""
        if self.first_name:
            name = name + self.first_name + " "
        if self.last_name:
            name = name + self.last_name
        if not name:
            name = "There"
        return name





class UserLoginActivity(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                    (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS,
                              choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'


class CreateAccount(TimeStampedModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    move = models.BooleanField(default=False)
    password = models.CharField(max_length=25,null=True,blank=True)

    months = models.IntegerField(default=0)
    pro = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Create Account'
        verbose_name_plural = 'Create Account'
