from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class About(models.Model):
    image_about = models.ImageField(upload_to = 'about')
    about_text = models.TextField()


class Contact(models.Model):
    firstname =  models.CharField(max_length=50)
    lastname =  models.CharField(max_length=50)
    contactnumber = models.CharField(max_length=11) 
    email = models.EmailField()
    message = models.TextField(default='')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


class usersave(models.Model):

    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    middle = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    email = models.EmailField()
    phoneno = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    cpassword = models.CharField(max_length=100)


class blogadd(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_image = models.ImageField(upload_to = 'blog')
    blog_detail = models.TextField()
    blog_date = models.DateTimeField(auto_now_add=True)