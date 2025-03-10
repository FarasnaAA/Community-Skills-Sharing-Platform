from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
class RegisterForm(forms.ModelForm):
    confirm_passowrd=forms.CharField(
        max_length=20,
        label="Re-enter password",
        widget=forms.PasswordInput(attrs={'id':'confirm_password','name':'confirm_password','placeholder':'Re enter the password'}),
    )
    class Meta:
        model = Register
        fields =['first_name','username','email','contact','password']
        widgets ={
            'first_name':forms.TextInput(attrs={'id':'first_name','name':'first_name','placeholder':'name'}),
            'username':forms.TextInput(attrs={'id':'username','name':'username','placeholder':'username'}),
            'email':forms.EmailInput(attrs={'id':'email','name':'email','placeholder':'email'}),
            'contact':forms.TextInput(attrs={'id':'contact','name':'contact','placeholder':'contact'}),
            'password':forms.PasswordInput(attrs={'id':'password','name':'password','placeholder':'password',}),
        }
        labels={
            'first_name':'Name',
            'username':'Username',
            'email':'Email-id',
            'contact':'Phone number',
            'password':'Password',
        }
        help_texts={
            'username':None
        }
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not username.isalnum():
            raise ValidationError("Username must only contain alphanumeric characters.")
        # Check if the username already exists (assuming you have a model named Register)
        if Register.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    # Custom Validation for email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Register.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email


            # Custom Validation for contact
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        contact_str = str(contact)  # Convert contact to string for validation
        if len(contact_str) != 10:
            raise ValidationError("Contact number must be exactly 10 digits.")
        if not contact_str.isdigit():
            raise ValidationError("Contact number must contain only digits.")
        return contact

    
    # Custom Validation for password
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError("Password must contain at least one letter.")
        return password
    
    # Custom Validation for confirm_password
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise ValidationError("Password and confirm password do not match.")
        return confirm_password
    

class LoginForm(forms.Form):
    username=forms.CharField(
        max_length=50,
        label="Username",
        widget=forms.TextInput(attrs={'id':'username','name':'username',}),
    )
    password=forms.CharField(
        max_length=20,
        label="Password",
        widget=forms.PasswordInput(attrs={'id':'password','name':'password',}),
    )




class EditProfileForm(forms.ModelForm):
    class Meta:
        model=Register
        fields=['first_name', 'username', 'email', 'contact','image']
        widgets={
            'first_name':forms.TextInput(attrs={'id':'first_name','name':'first_name'}),
            'username':forms.TextInput(attrs={'id':'username','name':'username'}),
            'email':forms.EmailInput(attrs={'id':'email','name':'email',}),
            'contact':forms.TextInput(attrs={'id':'contact','name':'contact'}),
            'image' : forms.FileInput(attrs={'id':'image','name':'image'}),
        }
        labels={
            'first_name':'FIRST NAME',
            'username':'USERNAME',
            'email':'EMAIL',
            'contact':'PHONE NUMBER',
            'image':'PROFILE PIC',
        }
        help_texts={
            'username':None
        }
    # Custom Validation for username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not username.isalnum():
            raise ValidationError("Username must only contain alphanumeric characters.")
        # Check if the username already exists (assuming you have a model named Register)
        if Register.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("This username is already taken.")

        return username
    
    # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact'))  # Ensure contact is a string
        if len(contact) != 10:
            raise ValidationError("Contact number must be exactly 10 digits.")
        if not contact.isdigit():
            raise ValidationError("Contact number must contain only digits.")
        return contact
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Register.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("An account with this email already exists.")
        return email
    



class ForgotPasswordForm(forms.Form):
    email=forms.CharField(max_length=50,label="",widget=forms.EmailInput(attrs={'id':'email','name':'email','placeholder':'Enter your E-mail'}))

class ResetPasswordForm(forms.Form):
    otp=forms.CharField(max_length=6,label="OTP",widget=forms.TextInput(attrs={'id':'otp','name':'otp','placeholder':'otp'}))
    newpassword=forms.CharField(max_length=50,label="New Password",widget=forms.PasswordInput(attrs={'id':'newpassword','name':'newpassword','placeholder':'Enter new password'}))
    confirmpassword=forms.CharField(max_length=50,label="Confirm Password",widget=forms.PasswordInput(attrs={'id':'confirmpassword','name':'confirmpassword','placeholder':'Enter confirm password'}))
    email=forms.CharField(max_length=50,label="E-mail",widget=forms.EmailInput(attrs={'id':'email','name':'email','placeholder':'Enter your E-mail'}))

    
           
#profilebio creation
   
class ProfileForm(forms.ModelForm):
    CHOICES = [
        ('male','male'),
        ('female','female'),
        ('other','other'),
        
    ]

    is_teacher = forms.BooleanField(
        required=False,
        label="I want to be a teacher",
        widget=forms.CheckboxInput(attrs={'id': 'is_teacher', 'name': 'is_teacher', 'class':"check"})
    )
    is_listener = forms.BooleanField(
        required=False,
        label="I want to be a listener",
        widget=forms.CheckboxInput(attrs={'id': 'is_listener', 'name': 'is_listener', 'class':"check"})
    )
    proof_document = forms.FileField(
    required=False,
    label="Upload Proof of Teaching (Required if applying as a teacher)",
    widget=forms.ClearableFileInput(attrs={'id': 'proof_document', 'name': 'proof_document', 'accept': 'video/*'})

    )
    gender = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect(attrs={'class':"check"}),
        label='Select gender'
    )
    skills = forms.CharField(
        widget=forms.TextInput(attrs={'id':'skills','name':'skills','placeholder':'Your skills (comma seperated)'}),
        label='Skills',
        required=False
    )
    interests = forms.CharField(
        widget=forms.TextInput(attrs={'id':'interests','name':'interests','placeholder':'Your interests(comma separated)'}),
        label='Interests',
        required=False
    )


    class Meta:
        model = Register
        fields = ['first_name', 'username', 'email', 'contact','gender', 'bio','interests','skills', 'is_teacher', 'is_listener', 'proof_document','image']
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'name': 'first_name', 'placeholder': 'Name'}),
            'username': forms.TextInput(attrs={'id': 'username', 'name': 'username', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email', 'placeholder': 'Email'}),
            'contact': forms.TextInput(attrs={'id': 'contact', 'name': 'contact', 'placeholder': 'Phone number'}),
            'bio': forms.Textarea(attrs={'id': 'bio', 'name': 'bio', 'placeholder': 'Tell us about yourself', 'rows': 3, 'cols':57}),
            'image' : forms.FileInput(attrs={'id':'image','name':'image'}),
        }
        labels = {
            'first_name': 'Name',
            'username': 'Username',
            'email': 'Email-id',
            'contact': 'Phone number',
            'gender':'gender',
            'bio': 'Bio',
            'interests':'Interests',
            'skills': 'Skills',
            'proof_document': 'Proof of Teaching',
            'image': 'Profile Picture',
        }
        help_texts={
            'username':None
        }

    def clean(self):
        cleaned_data = super().clean()
        is_teacher = cleaned_data.get('is_teacher')
        proof_document = cleaned_data.get('proof_document')

        # If user selects "Teacher" but doesn't upload proof, show error
        if is_teacher and not proof_document:
            self.add_error('proof_document', "You must upload a proof document to become a teacher.")
        
        return cleaned_data



    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not username.isalnum():
            raise ValidationError("Username must only contain alphanumeric characters.")
            # Check if the username already exists (assuming you have a model named Register)
        if Register.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("This username is already taken.")

        return username
    
    # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact'))  # Ensure contact is a string
        if len(contact) != 10:
            raise ValidationError("Contact number must be exactly 10 digits.")
        if not contact.isdigit():
            raise ValidationError("Contact number must contain only digits.")
        return contact
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Register.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("An account with this email already exists.")
        return email


class SkillForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        required=True
    )
    sub_category = forms.ModelChoiceField(
        queryset=Subcategory.objects.none(),
        empty_label="Select a Subcategory",
        required=True
    )
    additional_category = forms.ModelChoiceField(
        queryset=AdditionalCategory.objects.none(),
        empty_label="Select an Additional Category",
        required=True
    )

    # Add Payment Type field (Free or Paid)
    payment_type = forms.ChoiceField(
        choices=[('free', 'Free'), ('paid', 'Paid')],
        widget=forms.Select(attrs={'id': 'payment_type'})
    )

    # Add Price field (Only required if 'Paid' is selected)
    price = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'id': 'price', 'placeholder': 'Enter price'}),
        label="Price (for paid videos)"
    )


    class Meta:
        model = Skill
        fields = ['skill_name', 'category', 'sub_category', 'additional_category', 'skill_video', 'cover_image','payment_type', 'price']
        widgets = {
            'skill_name': forms.TextInput(attrs={'id': 'skill_name', 'name': 'skill_name', 'placeholder': 'SkillName'}),
            'cover_image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
        }
        labels = {
            'skill_name': 'Name',
            'category': 'Category',
            'sub_category': 'Sub Category',
            'additional_category': 'Additional Category',
            'skill_video': 'Video of Skill',
            'cover_image': 'Cover image for post',
        }

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        # Populate the category dropdown
        self.fields['category'].queryset = Category.objects.all()
        print(Category.objects.all()) 

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['sub_category'].queryset = Subcategory.objects.none()
        elif self.instance.pk:
            self.fields['sub_category'].queryset = Subcategory.objects.filter(category=self.instance.category)

        if 'sub_category' in self.data:
            try:
                subcategory_id = int(self.data.get('sub_category'))
                self.fields['additional_category'].queryset = AdditionalCategory.objects.filter(subcategory_id=subcategory_id)
            except (ValueError, TypeError):
                self.fields['additional_category'].queryset = AdditionalCategory.objects.none()
        elif self.instance.pk:
            self.fields['additional_category'].queryset = AdditionalCategory.objects.filter(subcategory=self.instance.sub_category)

    def clean(self):
        """ Ensure the selected subcategory and additional category belong to the chosen category """
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        sub_category = cleaned_data.get("sub_category")
        additional_category = cleaned_data.get("additional_category")
        payment_type = cleaned_data.get("payment_type")  # Ensure it's retrieved safely
        price = cleaned_data.get("price")

        if sub_category and sub_category.category != category:
            self.add_error("sub_category", "Selected subcategory does not belong to the chosen category.")

        if additional_category and additional_category.subcategory != sub_category:
            self.add_error("additional_category", "Selected additional category does not belong to the chosen subcategory.")


        # Ensure price is entered if the skill is paid
        if payment_type == "paid" and not price:
            self.add_error("price", "Please enter a price for paid skills.")


        return cleaned_data

    




    



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

class AdditionalCategoryForm(forms.ModelForm):
    class Meta:
        model = AdditionalCategory
        fields = ['name', 'subcategory']


