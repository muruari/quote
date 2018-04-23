from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def validate(self, postData):
        errors = []

        if len(postData.get('name')) < 3 or len(postData.get('alias')) < 3:
            is_valid = False
            errors.append('Name and Alias must have at least 3 characters each. Please try again.')

        if len(User.objects.filter(email = postData.get("email"))) > 0:
            is_valid = False
            errors.append('An account with that email address is already in use. Please try a different email address.')

        if not re.search(r'^[a-z" "A-Z]+$', postData.get('name')):
            is_valid = False
            errors.append('Name must be alphabetical characters only. Please try again.')

        if len(postData.get('password')) < 5:
            is_valid = False
            errors.append('Passwords must have at least 6 characters. Please try again.')

        if postData.get('password_confirmation') != postData.get('password'):
            is_valid = False
            errors.append('Passwords do not match. Please try again.')
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_of_birth = models.DateField(default = 'none')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __str__(self):
        return "name:{}, email:{}, password:{}, created_at:{}, updated_at:{}".format(self.name, self.email, self.password, self.created_at, self.updated_at)


class QuoteManager(models.Manager):
    def validate_quote(self, postData):
        errors = []

        if len(postData.get('quote_author')) < 2:
            is_valid = False
            errors.append('Quote Author must have at least 3 characters. Please try again.')

        if len(postData.get('quote_text')) < 9:
            is_valid = False
            errors.append('Quote Text must have at least 10 characters. Please try again.')

        return errors


class Quote(models.Model):
    quote_text = models.CharField(max_length = 255)
    quote_author = models.CharField(max_length = 255)    
    quotes = models.ManyToManyField(User, related_name="all_quotes")
    posted_by = models.ForeignKey(User, related_name="my_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()