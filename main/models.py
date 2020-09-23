from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first']) < 2:
            errors['first'] = 'You need at least 2 letters in your name'
        if len(postData['last']) < 2:
            errors['last'] = 'You need at least 2 letters in your name'
        if len(postData['pw']) < 8:
            errors['pw_length'] = "Password must be at least 8 characters"
        if postData['pw'] != postData['cPw']:
            errors['invalid_pw'] = 'Passwords do not match'
        if len(postData['email']) < 8:
            errors['email_length'] = 'Email is not long enough'
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) < 8:
            errors['email_length'] = 'Email is not long enough'
        user = User.objects.get(email=postData['email'])  
        if bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
            print("password match")
        else:
            errors['incorrect'] = "Email or Password is incorect"
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        return errors

class User(models.Model):
    first = models.CharField(max_length=45)
    last = models.CharField(max_length=45)
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f'{self.first} {self.last}'



class Listing(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    img = models.FileField()
    posted_by = models.ForeignKey(User, related_name='posted', on_delete=models.CASCADE)
    price = models.IntegerField()
    condition = models.CharField(max_length=10)
    location = models.CharField(max_length=15)
    watching = models.ManyToManyField(User, related_name='watching')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name + ": " + str(self.imagefile)

class Comment(models.Model):
    comment = models.TextField(max_length=200)
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

