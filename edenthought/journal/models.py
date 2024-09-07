from django.db import models

from django.contrib.auth.models import User


class Thought(models.Model):

    Title = models.CharField(max_length=250)
    Content = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)


class Profile(models.Model):

    profile_pic = models.ImageField(null=True, blank=True, default='Default-Profile-Picture.png')
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)
