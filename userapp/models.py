from django.db import models
from django.contrib.auth.models import AbstractUser

class Register(AbstractUser):
    usertype = models.CharField(max_length=50,default="admin")
    contact = models.IntegerField(null=True)
    image = models.ImageField(upload_to='uploads/',null=True)
    bio = models.TextField(max_length=500,null=True)
    interests = models.TextField(max_length=100,null=True)
    skills = models.TextField(max_length=100,null=True)
    proof_document = models.FileField(upload_to='proof_videos/', null=True, blank=True)  # Accepts videos)
    is_listener = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    gender = models.CharField(max_length=50,null=True)
    full_name = models.CharField(max_length=100, null=True) 
    is_approved = models.BooleanField(default=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)



    

# Create your models here.
class Reset(models.Model):
    otp = models.CharField(max_length=6, null=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE,null=True)
    otp_created_at = models.DateTimeField(auto_now_add =True)


# message table
class Message(models.Model):
    is_following = models.BooleanField(default=False)
    message = models.CharField(max_length=100, null=True)
    follower = models.ForeignKey(Register, on_delete=models.CASCADE,null=True,related_name="follower")
    message_created_at = models.DateTimeField(auto_now_add =True)
    followee = models.ForeignKey(Register, on_delete=models.CASCADE,null=True,related_name="followee")
    response = models.CharField(max_length=100, null=True)


#skill table
class Skill(models.Model):
     user = models.ForeignKey(Register, on_delete=models.CASCADE,null=True)
     skill_name = models.CharField(max_length=100, null=True)
     CATEGORY_CHOICES = [
        ('Tech', 'Technology'),
        ('Art', 'Arts'),
        ('Music', 'Music'),
        ('Cooking', 'Cooking'),
        ('Fitness', 'Fitness'),
        ('Other', 'Other')
    ]
     category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True)
     sub_category = models.CharField(max_length=100, null=True)
     skill_created_at = models.DateTimeField(auto_now_add =True)
     skill_video = models.FileField(upload_to='skill_videos/', null=True, blank=True)
     cover_image = models.ImageField(upload_to='uploads/',null=True, blank=True)


