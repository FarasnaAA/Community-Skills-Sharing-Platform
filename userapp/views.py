from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
import secrets,string
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Message, Register 
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
import uuid
from urllib.parse import unquote
from django.db.models import Sum



def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def classes(request):
    return render(request,'classes.html')
def contact(request):
    return render(request,'contact.html')
def facility(request):
    return render(request,'facility.html')


def reg(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form)
        
        if form.is_valid():
            email=form.cleaned_data['email']
            print(email)
            data=Register.objects.filter(email=email)
            print(data)
            if data:
                messages.eror(request,"email id exists",exter_tags="error")
                return redirect('user_login')
            else:
                user=form.save(commit=False)
                user.usertype="user"
                user.password=make_password(form.cleaned_data['password'])
                user.save()
                messages.success(request,"register successfull",extra_tags="success")
                return redirect('user_login')
        else :
             print(form.errors)
             messages.error(request,"Registration failed!!",extra_tags="error")
             form=RegisterForm()
             return render(request,'reg.html',{'form':form,'title':'Register','button':'Register'})
        
    else:
        form=RegisterForm()
        
    return render(request,'reg.html',{'form':form,'title':'Register','button':'Register'})

def user_login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                users=Register.objects.get(username=user)
                request.session['ut']=users.usertype
                request.session['uid']=users.id
                request.session['uname']=users.username
                messages.success(request,"login successfull",extra_tags="success")
                return redirect('/')
            else :
                messages.error(request,"indirect username and password",extra_tags="error")
        else:
            messages.error(request,"login faild",extra_tags="error")
            form=LoginForm()
            return render(request,'user_login.html',{'form':form})
    else:
        form=LoginForm()
    return render(request,'user_login.html',{'form':form})

def home(request):
    return render(request,'home.html')

def user_logout(request):
    logout(request)
    messages.success(request,"logout successfully",extra_tags="successs")
    return redirect('/')





def view_user(request):
    users = Register.objects.filter(usertype="user")
    return render(request,'users.html',{'users':users})


def profile(request):
    user=request.user
    user = Register.objects.get(id=user.id)
    return render(request,'profile.html',{'user':user})


def edit_profile(request):
    user = Register.objects.get(id=request.user.id) 
    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevent user from being logged out
            messages.success(request, "Profile updated successfully.", extra_tags="success")
            return redirect('profile')  # Redirect to the profile page
        else:
            messages.error(request, "Profile update failed. Please check your form.", extra_tags="error")
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'reg.html', {'form': form,'title':'Edit Profile','button':'Update'})




def forgot_password(request):
    if request.method == 'POST':
        print("1")
        form=ForgotPasswordForm(request.POST)
        if form.is_valid():
            print("2")
            email=form.cleaned_data['email']
            data=Register.objects.filter(email=email)
            if data:
                print("3")
                new_password=generate_random_password()
                user=Register.objects.get(email=email)
                Reset.objects.create(otp=new_password,user=user)
                subject="Password Reset Request"
                message=f'Your one time password is {new_password}'
                email_from=settings.EMAIL_HOST_USER
                email_to=[email]
                send_mail(subject,message,email_from,email_to)
                messages.success(request, "OTP has been sent to your mail.", extra_tags="success")
                return redirect ('reset_password')
            else:
                print("4")
                messages.error(request, "Invalid E_mail ", extra_tags="error")
        else:
            print("5")
            messages.error(request, "Invalid Form", extra_tags="error")
    else:
        print("6")
        form=ForgotPasswordForm()
    return render(request,'forgot_password.html',{'form':form})



def generate_random_password(length=6):
    characters=string.ascii_letters+string.digits
    password=''.join(secrets.choice(characters) for _ in range(length))
    return password



def reset_password(request):
    if request.method == 'POST':
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            otp=form.cleaned_data['otp']
            email=form.cleaned_data['email']
            user = Register.objects.get(email=email)
            user_otp=Reset.objects.filter(user=user).first()
            if user_otp.otp == otp:
                newpassword=form.cleaned_data['newpassword']
                data=Register.objects.get(id=user.id)
                data.password=make_password(newpassword)
                data.save()

                user_otp.delete()

                messages.success(request,"Password changed", extra_tags="success")
                return redirect('user_login')
            else:
                messages.error(request,"Inavalid otp", extra_tags="error")
        else:
            messages.error(request,"Inavalid form data", extra_tags="error")
    else:
        form=ResetPasswordForm()
    return render(request,'reset_password.html',{'form':form})


#delete user
    
def delete_user(request,id):
    user=Register.objects.get(id=id)
    subject="Account Deletion Notification"
    message=f"Dear {user.username} Your account is being deleted. You will no longer have access to your account. Please register again for future use..."
    email_from=settings.EMAIL_HOST_USER
    email_to=[user.email]
    send_mail(subject, message, email_from, email_to)

    user.delete()
    messages.success(request,'user deleted successfully',extra_tags='success')
    return redirect('view_user')


# edit profile details include bio

def profile_page(request):
    user = Register.objects.get(id=request.user.id)
    #     # Fetch course history
    # attended_courses = Skill.objects.filter(user=user, status="Completed")
    # pending_courses = Skill.objects.filter(user=user, status="Pending") 


    #     # Fetch payment details
    # payments = Payment.objects.filter(user=user)


    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False
            user.save()
            update_session_auth_hash(request, user)  # Prevent user from being logged out
            messages.success(request, "Profile updated successfully.", extra_tags="success")
            return redirect('profile')  # Redirect to the profile page
        else:
            messages.error(request, "Profile update failed. Please check your form.", extra_tags="error")
    else:
        form = ProfileForm(instance=user)
        
    

    return render(request, 'reg.html', {'form': form,
        'user': user,'title':'Update Profile','button':'Update'})
        # 'attended_courses': attended_courses,
        # 'pending_courses': pending_courses,
        # 'payments': payments,
        # 'title': 'Profile Dashboard'})



#view users for admin

def view_profile(request):
    users = Register.objects.filter(usertype="user")
    return render(request,'users.html',{'users':users})

def approve_teachers(request,id):
    user=Register.objects.get(id=id)
    subject="Account Approval Notification"
    message=f"Dear {user.username} Your account is verified as Teacher as per the approval of your proof of document.Kindly welcome to our platform and feel free to teach to others.all the best!!!"
    email_from=settings.EMAIL_HOST_USER
    email_to=[user.email]
    send_mail(subject, message, email_from, email_to)

    user.is_approved = True
    user.save()
    messages.success(request,'Teacher approved successfully',extra_tags='success')
    return redirect('view_profile')


def reject_teachers(request,id):
    user=Register.objects.get(id=id)
    subject="Account Rejection Notification"
    message=f"Dear {user.username} Your registration as a teacher is being Rejected. Please register again with valid proof or continue with the platform as a listener...."
    email_from=settings.EMAIL_HOST_USER
    email_to=[user.email]
    send_mail(subject, message, email_from, email_to)

    user.delete()
    messages.success(request,'user rejected successfully',extra_tags='success')
    return redirect('view_profile')



#view profiles(hub) and search
def view_profiles(request):
    current_user = request.user
    query = request.GET.get('q', '')

    users = Register.objects.exclude(id=current_user.id).exclude(is_superuser=True)

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(full_name__icontains=query) |
            Q(bio__icontains=query) |
            Q(interests__icontains=query) |
            Q(skills__icontains=query)
        )

        if query.lower() == "teacher":
            users = Register.objects.filter(is_teacher=True)
        elif query.lower() == "listener":
            users = Register.objects.filter(is_listener=True)

    # Attach follow status to each user
    for user in users:
        user.is_following = Message.objects.filter(follower=current_user, followee=user, is_following=True).exists()

    return render(request, 'view_profiles.html', {'users': users, 'query': query})







#follow
def follow(request, id):
    """Follow or Unfollow a user and reload the page."""
    if request.user.is_authenticated:
        followee = get_object_or_404(Register, id=id)  # User to follow/unfollow
        follower = request.user  # Logged-in user

        try:
            message, created = Message.objects.get_or_create(follower=follower, followee=followee)
            message.is_following = not message.is_following  # Toggle follow status
            message.save()
        except MultipleObjectsReturned:
            message = Message.objects.filter(follower=follower, followee=followee).first()
            message.is_following = not message.is_following
            message.save()
    return redirect(request.META.get('HTTP_REFERER', 'view_profiles'))  # Redirect to the same page



#followiee profile card view
@login_required
def followeprofile_view(request, id):
    followee = get_object_or_404(Register, id=id)  # The user being viewed
    follower = request.user  # The logged-in user

    # Check if the user is already following
    follow_relationship = Message.objects.filter(follower=follower, followee=followee, is_following=True).first()
    is_following = follow_relationship is not None
    followers_list = []
    following_list = []
    followee_skills = [] 
    followee_posts = []
    if is_following:
       followers_list = Message.objects.filter(followee=followee, is_following=True).select_related('follower')
        # Following List (People whom the followee follows)
       following_list = Message.objects.filter(follower=followee, is_following=True).select_related('followee')
       followee_skills = Skill.objects.filter(user=followee).order_by('skill_created_at')

    for skill in followee_skills:
            skill.is_paid = Payment.objects.filter(user=follower, skill=skill, status="completed").exists()

 

    if request.method == "POST":
        if is_following:
            # Unfollow: Set is_following to False instead of deleting
            follow_relationship.is_following = False
            follow_relationship.save()
        else:
            # Follow: Create a new Message instance with is_following=True
            Message.objects.create(follower=follower, followee=followee, is_following=True)

        return redirect('followeprofile_view', id=id)

    context = {
        'followee': followee,
        'is_following': is_following,
        'followers_count': Message.objects.filter(followee=followee, is_following=True).count(),
        'following_count': Message.objects.filter(follower=followee, is_following=True).count(),
        'followers_list': followers_list,  # Pass followers list to template
        'following_list': following_list,  # Pass following list to template
        'followee_skills' :  followee_skills,
    }
    return render(request, 'view_followepro.html', context)






#messaging between users


@login_required
def message_user(request, id):
    followee = get_object_or_404(Register, id=id)  # Get recipient

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            Message.objects.create(
                follower=request.user,
                followee=followee,
                message=message_text
            )
        return JsonResponse({"success": True})  # ✅ Prevents redirection issue

    messages = Message.objects.filter(
        Q(follower=request.user, followee=followee) | 
        Q(follower=followee, followee=request.user)
    ).order_by('message_created_at')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # ✅ AJAX request
        return JsonResponse({
            "messages": [
                {
                    "text": msg.message,
                    "timestamp": msg.message_created_at.strftime("%b %d, %H:%M"),
                    "sender": msg.follower == request.user
                } 
                for msg in messages
            ]
        })

    return render(request, 'message_user.html', {'followee': followee, 'messages': messages})



#toggle for following and follow
@login_required
def toggle_follow(request, id):
    followee = get_object_or_404(Register, id=id)  # Get the user to follow/unfollow
    follower = request.user  # Get the current logged-in user

    # Check if already following
    follow_relationship = Message.objects.filter(follower=follower, followee=followee)

    if follow_relationship.exists():
        follow_relationship.delete()  # Unfollow
    else:
        Message.objects.create(follower=follower, followee=followee, is_following=True)  # Follow

    return redirect('view_profiles')  # Redirect to the hub page


def delete_message(request, message_id):
    if request.method == "POST":
            message = get_object_or_404(Message, id=message_id)

            # ✅ Fix: Ensure only the sender can delete the message
            if message.follower == request.user:
                message.delete()

            # Redirect to the message page
            return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})  # If GET request, redirect ba



#chat list
@login_required
def chat_list(request):
    user = request.user
    chats = Message.objects.filter(followee=user).values('follower').distinct()  # Get unique followers

    chat_users = []
    for chat in chats:
        last_message = Message.objects.filter(follower_id=chat['follower'], followee=user).order_by('-message_created_at').first()
        unread_count = Message.objects.filter(follower_id=chat['follower'], followee=user, is_read=False).count()  # Count unread messages per user

        chat_users.append({
            'follower': last_message.follower,
            'last_message': last_message.message,
            'time': last_message.message_created_at,
            'unread_count': unread_count
        })
        unread_count_total = Message.objects.filter(followee=user, is_read=False).count()  # Total unread messages
        

    return render(request, 'chat_list.html', {'chat_users': chat_users})


# def unread_messages_count(request):
#     if request.user.is_authenticated:
#         unread_count = Message.objects.filter(followee=request.user, is_read=False).count()
#     else:
#         unread_count = 0
#     return {'unread_count': unread_count}



#post skills:
@login_required
def post_skill(request):


    user = Register.objects.get(id=request.user.id)


    # Restrict skill posting to only teachers
    if not user.is_teacher:
        messages.error(request, "Only teachers can post skills.")
        return redirect('profile') 
        

    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES)

        # Validate uploaded video format
        skill_video = request.FILES.get('skill_video')
        allowed_formats = ['video/mp4', 'video/avi', 'video/mkv']
        if skill_video and skill_video.content_type not in allowed_formats:
            messages.error(request, "Invalid video format. Upload MP4, AVI, or MKV.")
            return redirect('post_skill')

        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = user
            # Check if it's paid but no price is set
            if skill.payment_type == 'paid' and not skill.price:
                messages.error(request, "Please set a price for the paid skill.")
                return redirect('post_skill')
  
            skill.save()
            messages.success(request, "Skill posted successfully.")
            return redirect('profile')  
        else:
            messages.error(request, "Failed to post skill. Please check the form.")

       
    else:
        form = SkillForm()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    additional_categories = AdditionalCategory.objects.all()
    
    return render(request, 'post_skill.html', {'form': form,
    'categories': categories,
    'subcategories': subcategories,
    'additional_categories': additional_categories})


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    else:
        subcategories = Subcategory.objects.none()  # Return an empty queryset if no category is selected
    return JsonResponse(list(subcategories), safe=False)

def load_additional_categories(request):
            subcategory_id = request.GET.get('subcategory_id')
            additional_categories = AdditionalCategory.objects.filter(subcategory_id=subcategory_id).values('id', 'name')
            return JsonResponse(list(additional_categories), safe=False)   

#check payment status
@login_required
def check_payment_status(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    has_paid = Payment.objects.filter(user=request.user, skill=skill, status="completed").exists()
    return JsonResponse({"has_paid": has_paid})



#view skill for edit

def view_skill(request):
    user=request.user
    user_skills = Skill.objects.filter(user=user)  # Fetch skills of the user
    return render(request, 'view_skill.html', {'user_skills': user_skills})

#edit skill

def edit_skill(request, id):
    skill = get_object_or_404(Skill, id=id)  # Get skill by ID

    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('view_skill')  # Redirect to skill view page
    else:
        form = SkillForm(instance=skill)  # Pre-fill form with skill data

    return render(request, 'edit_skill.html', {'form': form})





#category list:
@login_required
def category_list(request):
    """Show all unique categories as cards."""
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)

    return render(request, 'subcategory_list.html', {
        'category': category,
        'subcategories': subcategories  # Ensure this matches the template
    })


@login_required
def additionalcategory_list(request, subcategory_id):
    sub_category = get_object_or_404(Subcategory, id=subcategory_id)
    additional_categories = AdditionalCategory.objects.filter(subcategory=sub_category)

    for additional in additional_categories:
        print(f"Additional Category: {additional.name}, ID: {additional.id}")  # Debugging

    return render(request, 'additionalcategory_list.html', {
        'subcategory': sub_category,
        'additional_categories': additional_categories
    })

# Show skills under a subcategory
@login_required
def skill_list(request, additionalcategory_id):
    print(additionalcategory_id)
    additional_category = get_object_or_404(AdditionalCategory, id=additionalcategory_id)
    print(additional_category.id)


    # Filter skills where sub_category matches the selected subcategory name
    skill_videos = Skill.objects.filter(additional_category=additional_category).order_by('id')
    print(skill_videos)
    paid_skill_ids = set(
        Payment.objects.filter(user=request.user, status="Completed").values_list("skill_id", flat=True)
    )

    # Add an attribute to check if the user has paid for each skill
    for skill in skill_videos:
        skill.is_paid = skill.id in paid_skill_ids


    return render(request, 'skill_list.html', {
        'additionalcategory' : additional_category,
        'skill_videos': skill_videos,
    })



#add category
@login_required
def add_category(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()  # Get all subcategories for dropdown
    additional_categories = AdditionalCategory.objects.all()  # Fetch all additional categories



    if request.method == "POST":
        if 'category_submit' in request.POST:  # Add Category
            category_name = request.POST.get('category_name')
            if category_name:
                Category.objects.create(name=category_name)
                return redirect('add_category')

        elif 'subcategory_submit' in request.POST:  # Add Subcategory
            subcategory_name = request.POST.get('subcategory_name')
            category_id = request.POST.get('category')

            if subcategory_name and category_id:
                category = Category.objects.get(id=category_id)
                Subcategory.objects.create(name=subcategory_name, category=category)
                return redirect('add_category')
            
        elif 'additional_category_submit' in request.POST:  # Add Additional Category
            additional_category_name = request.POST.get('additional_category_name')
            subcategory_id = request.POST.get('subcategory')

            if additional_category_name and subcategory_id:
                subcategory = Subcategory.objects.get(id=subcategory_id)
                AdditionalCategory.objects.create(name=additional_category_name, subcategory=subcategory)
                return redirect('add_category')

    return render(request, 'admin_category.html', {
        'categories': categories,
        'subcategories': subcategories,
        'additional_categories': additional_categories  # Pass additional categories to the template
    })

@login_required
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('add_category')


def edit_all_categories(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    additional_categories = AdditionalCategory.objects.all()

    if request.method == "POST":
        category_forms = [CategoryForm(request.POST, instance=category) for category in categories]
        subcategory_forms = [SubCategoryForm(request.POST, instance=subcategory) for subcategory in subcategories]
        additional_category_forms = [AdditionalCategoryForm(request.POST, instance=additional_category) for additional_category in additional_categories]

        all_forms = category_forms + subcategory_forms + additional_category_forms

        if all(form.is_valid() for form in all_forms):
            for form in all_forms:
                form.save()
            return redirect('add_category')

    else:
        category_forms = [CategoryForm(instance=category) for category in categories]
        subcategory_forms = [SubCategoryForm(instance=subcategory) for subcategory in subcategories]
        additional_category_forms = [AdditionalCategoryForm(instance=additional_category) for additional_category in additional_categories]

    return render(request, 'edit_all_category.html', {
        'category_forms': category_forms,
        'subcategory_forms': subcategory_forms,
        'additional_category_forms': additional_category_forms
    })



#payment section:
def payment_confirmation(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    return render(request, 'payment_confirmation.html', {'skill': skill})


def make_payment(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    return render(request, 'payment.html', {'skill': skill})


def process_payment(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect("make_payment", skill_id=skill.id)
        
        if payment_method == "Credit Card":
            return redirect('confirm_credit_card_payment', skill_id=skill_id)
        elif payment_method == "UPI":
            return redirect('upi_selection', skill_id=skill_id)

        # Simulating a payment success for now (Replace with real payment gateway logic)
        transaction_id = str(uuid.uuid4())  # Generating a unique transaction ID
        payment_status = "Success"  # Change this dynamically based on payment response

        # Store payment details in the database
        payment = Payment.objects.create(
            user=request.user,
            skill=skill,
            amount=skill.price,
            payment_method=payment_method,
            status=payment_status,
            transaction_id=transaction_id
        )

       # Simulate real payment processing (Replace with actual payment gateway integration)
        payment_gateway_response = "Success"  # Change this dynamically based on payment response

        if payment_gateway_response == "Success":
            payment.status = "Success"
            messages.success(request, "Payment successful! You can now access the course.")
        elif payment_gateway_response == "Failed":
            payment.status = "Failed"
            messages.error(request, "Payment failed. Please try again.")
        elif payment_gateway_response == "Refund":
            payment.status = "Refund"
            messages.info(request, "Your payment has been refunded.")
        else:
            payment.status = "Pending"  # Default case

        payment.save()  # Save the updated status in the database

        return redirect("skill_list" if payment.status == "Success" else "make_payment", skill_id=skill.id)


    return render(request, "payment.html", {"skill": skill})


def confirm_credit_card_payment(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    errors = {}  # Dictionary to store field-specific validation errors

    if request.method == "POST":
        card_number = request.POST.get("card_number", "").strip().replace(" ", "")
        expiry_date = request.POST.get("expiry_date", "").strip()
        cvv = request.POST.get("cvv", "").strip()
        cardholder_name = request.POST.get("cardholder_name", "").strip()

        # Validate Card Number (Must be exactly 16 digits)
        if not card_number:
            errors["card_number"] = "Card number is required."
        elif not card_number.isdigit() or len(card_number) != 16:
            errors["card_number"] = "Invalid card number! Must be exactly 16 digits."

        # Validate Expiry Date (Must be in MM/YY format)
        expiry_pattern = r"^(0[1-9]|1[0-2])\/(\d{2})$"
        if not expiry_date:
            errors["expiry_date"] = "Expiry date is required."
        elif not re.match(expiry_pattern, expiry_date):
            errors["expiry_date"] = "Invalid expiry date! Use MM/YY format."

        # Validate CVV (Must be 3 or 4 digits)
        if not cvv:
            errors["cvv"] = "CVV is required."
        elif not cvv.isdigit() or len(cvv) not in [3, 4]:
            errors["cvv"] = "Invalid CVV! Must be 3 or 4 digits."

        # Validate Cardholder Name (Only alphabets and spaces allowed)
        if not cardholder_name:
            errors["cardholder_name"] = "Cardholder name is required."
        elif not re.match(r"^[A-Za-z\s]+$", cardholder_name):
            errors["cardholder_name"] = "Invalid name! Only alphabets and spaces are allowed."

        # If there are errors, re-render the form with error messages
        if errors:
            return render(request, "credit_card_payment.html", {"skill": skill, "errors": errors})

        # Simulating a payment success (Integrate real payment gateway here)
        transaction_id = str(uuid.uuid4())  
        payment_status = "Success"

        # Save Payment
        Payment.objects.create(
            user=request.user,
            skill=skill,
            amount=skill.price,
            payment_method="Credit Card",
            status=payment_status,
            transaction_id=transaction_id
        )

        messages.success(request, "Payment successful! You can now access the course.")
        return redirect("payment_success",transaction_id=transaction_id, amount=skill.price)  

    return render(request, "credit_card_payment.html", {"skill": skill, "errors": {}})



def payment_success(request, transaction_id, amount):
    return render(request, 'payment_success.html', {
        'transaction_id': transaction_id,
        'amount': amount
    })
   


def view_receipt(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    
    # Get the teacher's name (update based on your actual model structure)
    teacher_name = payment.skill.user.first_name if payment.skill else "Unknown"

    # Get the user who made the payment
    from_user = payment.user.username  
    course_name = payment.skill.skill_name  # The purchased course

    # Determine the payment method (Assuming 'payment_method' is stored in the Payment model)
    payment_method = payment.payment_method if hasattr(payment, "payment_method") else "Unknown"

    context = {
        "payment": payment,
        "to_user": teacher_name,
        "from_user": from_user,
        "course_name": course_name,
        "payment_method": payment_method,  # Include payment method in the receipt
    }
    
    return render(request, "receipt.html", context)




def upi_selection(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == "POST":
        upi_option = request.POST.get("upi_option")

        if not upi_option:
            messages.error(request, "Please select a UPI option.")
            return redirect("upi_selection", skill_id=skill.id)

        # Redirect to UPI Payment Page with selected option
        return redirect("upi_payment", skill_id=skill.id, upi_option=upi_option)

    return render(request, "upi_selection.html", {"skill": skill})




def upi_payment(request, skill_id, upi_option):
    skill = get_object_or_404(Skill, id=skill_id)

    # Decode the UPI option to handle URL encoding
    upi_option = unquote(upi_option)

    return render(request, "upi_payment.html", {"skill": skill, "upi_option": upi_option})






def confirm_upi_payment(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    transaction_id = str(uuid.uuid4())  # Generate a unique transaction ID
    payment_status = "Success"  # ✅ Change status to "Success"

    # Store payment details
    payment = Payment.objects.create(
        user=request.user,
        skill=skill,
        amount=skill.price,
        payment_method="UPI",
        status=payment_status,
        transaction_id=transaction_id
    )

    messages.success(request, "UPI Payment recorded! Admin will verify soon.")
    return redirect("view_receipt" , transaction_id=transaction_id)





#payment history
@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user, status='Success')  # Fetch only successful payments
    return render(request, 'payment_history.html', {'payments': payments})



#view course video after payment
def view_course_video(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id, status="Success")
     # Check if payment was successful
    if payment.status != "Success":
        return redirect('payment_failed_page')  # Redirect users who haven't paid


    return render(request, 'course_video.html', {'payment': payment})

#teacher earnings
def teacher_earnings(request):
    teacher = request.user  # Get the logged-in teacher
    earnings = Payment.objects.filter(skill__user=teacher)  # Adjust if needed

    total_earnings = earnings.aggregate(Sum('amount'))['amount__sum'] or 0
    pending_balance = earnings.filter(status="Pending").aggregate(Sum('amount'))['amount__sum'] or 0

    completed_payments = Payment.objects.filter(status="Completed").select_related('user', 'skill')

    return render(request, 'teacher_earnings.html', {
        'total_earnings': total_earnings,
        'pending_balance': pending_balance,
        'completed_payments': earnings
    })

#show earnings and payment selection for teachers
def teacher_payment_selection(request):
    return render(request, 'teacher_payment_selection.html')