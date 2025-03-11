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
    is_read = models.BooleanField(default=False)  # Add this field


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
     additional_category = models.CharField(max_length=100, null=True)
     skill_created_at = models.DateTimeField(auto_now_add =True)
     skill_video = models.FileField(upload_to='skill_videos/', null=True, blank=True)
     cover_image = models.ImageField(upload_to='uploads/',null=True, blank=True)
     payment_type = models.CharField(max_length=10,  default='free')
     price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # Store price for paid videos
     paid_users = models.ManyToManyField(Register,related_name="paid_skills", blank=True)  # Track users who paid


     def has_paid(self, user):
        return self.paid_users.filter(id=user.id).exists()




# Category Model (All Main Skills)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name  # This ensures the category name is displayed


# SubCategory Model (Belongs to a Category)
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    

class AdditionalCategory(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="additional_categories")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    




class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),  # Default status
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Refund', 'Refund')  # New refund status
    ]
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # The user making the payment
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)  # The skill being purchased
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    payment_method = models.CharField(max_length=50)  # Payment method
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Updated default status
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Unique transaction ID
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment

    def __str__(self):
        return f"{self.user.username} - {self.skill.skill_name} - {self.status}"
