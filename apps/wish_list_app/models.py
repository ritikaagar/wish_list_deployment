from __future__ import unicode_literals
from django.db import models
import re
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) <3:
            errors['name'] = "Name field should include at least 3 characters"
        if len(postData['username']) < 3:
            errors['username'] = "Username field should include at least 3 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password field must include at least 8 characters"
        if postData['password'] != postData['password_conf']:
            errors['password_conf'] = "Password field must match Confirm PW field"
        if errors:
            return errors
        else:
            pass

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class ItemManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors['item'] = "'Item:' field should contain at least 3 characters"
            return errors
        else:
            pass

class Item(models.Model):
    item = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name = "posters")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    users = models.ManyToManyField(User, related_name="items")
    objects = ItemManager()