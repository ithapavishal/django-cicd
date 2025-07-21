import re
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail

from .models import Profile
from .forms import ProfileForm

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str



'''
# Update RegisterView
class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        role = request.POST.get('role')

        valid_roles = ['admin', 'instructor', 'student']
        if role not in valid_roles:
            messages.error(request, "Invalid role selected.")
            return redirect('register')

        try:
            if username.lower() in password.lower():
                messages.error(request, "Your password is too similar to username")
                return redirect('register')
            
            if not re.search(r"[A-Z]", password):
                messages.error(request, "Your password must contain at least one uppercase letter")
                return redirect('register')

            if not re.search(r"\d", password):
                messages.error(request, "Your password must contain at least one digit")
                return redirect('register')

            validate_password(password)
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                else:
                    user = User.objects.create_user(
                        first_name=first_name, 
                        last_name=last_name, 
                        username=username, 
                        email=email, 
                        password=password
                    )

                    if role in ['admin', 'instructor']:
                        token = default_token_generator.make_token(user)
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        approval_link = request.build_absolute_uri(
                            reverse('approve_user', kwargs={'uidb64': uid, 'token': token})
                        )

                        subject = f"New {role.capitalize()} Registration - Approval Required"
                        message = render_to_string('accounts/email_approval.html', {
                            'user': user,
                            'role': role.capitalize(),
                            'approval_link': approval_link,
                            'date': timezone.now(),
                        })
                        from_email = "ivishalthapa21@gmail.com"
                        recipient_list = ['v01.thapa@gmail.com']  # Replace with actual admin email

                        send_mail(subject, strip_tags(message), from_email, recipient_list, fail_silently=False)
                        messages.success(request, f"{first_name}, your registration as an {role} is pending approval.")
                    else:
                        Profile.objects.create(user=user, role='student')
                        messages.success(request, 'User registered successfully.')

                    return redirect('login')
            else:
                messages.error(request, "Passwords do not match")
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
        
        return redirect('register')

# New view to handle user approval by admin
class ApproveUserView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            profile = Profile.objects.get(user=user)
            context = {'user': user, 'profile': profile}
            return render(request, 'accounts/approve_user.html', context)
        else:
            messages.error(request, "Invalid approval link.")
            return redirect('home')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            profile = Profile.objects.get(user=user)
            approve = request.POST.get('approve') == 'yes'

            if approve:
                profile.is_approved = True
                profile.save()
                subject = "Your account has been approved"
                message = "Congratulations! Your account has been approved and you can now log in."
            else:
                user.delete()
                subject = "Your account registration has been rejected"
                message = "Sorry, your account registration has been rejected."

            send_mail(subject, message, 'ivishalthapa21@gmail.com', [user.email], fail_silently=False)
            messages.success(request, f'User {user.username} has been {"approved" if approve else "rejected"}.')
            return redirect('home')
        else:
            messages.error(request, "Invalid approval link.")
            return redirect('home')
'''

# Create your views here.

# @login_required(login_url="log_in")
# def profile(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     profile_form = ProfileForm(instance=profile)

#     if request.method == "POST":
#         profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Profile updated successfully')
#             return redirect("profile")

#     context = {
#         'profile_form': profile_form,
#         'user': request.user,
#         'profile': request.user.profile
#     }
#     return render(request, 'accounts/profile.html', context)

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        role = request.POST.get('role')  # Get the role from the form
        
        # Validate roles
        valid_roles = ['admin', 'instructor', 'student']
        if role not in valid_roles:
            messages.error(request, "Invalid role selected.")
            return redirect('register')

        try:
            if username.lower() in password.lower():
                messages.error(request, "Your password is too similar to username")
                return redirect('register')
            
            if not re.search(r"[A-Z]", password):
                messages.error(request, "Your password must contain at least one uppercase letter")
                return redirect('register')

            if not re.search(r"\d", password):
                messages.error(request, "Your password must contain at least one digit")
                return redirect('register')

            validate_password(password)
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                else:
                    user = User.objects.create_user(
                        first_name=first_name, 
                        last_name=last_name, 
                        username=username, 
                        email=email, 
                        password=password
                    )

                    if role == 'admin':
                        # Check if there is already an admin
                        if not Profile.objects.filter(role='admin').exists():
                            # First admin registration, approve automatically
                            Profile.objects.create(user=user, role='admin', is_approved=True)
                            messages.success(request, 'First admin registered successfully.')
                        else:
                            # Subsequent admin registrations, send for approval
                            Profile.objects.create(user=user, role='admin', is_approved=False)
                            # Send email to the admin for approval
                            subject = f"New Admin Registration - Approval Required"
                            message = render_to_string('accounts/email_approval.html', {
                                'user': user,
                                'role': 'Admin',
                                'date': timezone.now(),
                            })
                            from_email = "ivishalthapa21@gmail.com"
                            recipient_list = ['ivishalthapa21@gmail.com']  # Replace with the actual admin email
                            
                            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                            messages.success(request, f"{first_name}, your registration as an admin is pending approval.")
                    elif role == 'instructor':
                        # All instructors need approval
                        Profile.objects.create(user=user, role='instructor', is_approved=False)
                        # Send email to the admin for approval
                        
                        # profile_url = request.build_absolute_uri(reverse('profile_action', kwargs={'user_id': user.id, 'action': 'approve'}))
                        # reject_url = request.build_absolute_uri(reverse('profile_action', kwargs={'user_id': user.id, 'action': 'reject'}))
                        admin_dashboard_url = request.build_absolute_uri(reverse('admin_dashboard'))

                        subject = f"New Instructor Registration - Approval Required"
                        html_message = render_to_string('accounts/email_approval.html', {
                            'user': user,
                            'role': 'Instructor',
                            'date': timezone.now(),
                            # 'profile_url': profile_url,
                            # 'reject_url': reject_url,
                            'admin_dashboard_url': admin_dashboard_url,
                        })
                        plain_message = strip_tags(html_message)
                        from_email = "ivishalthapa21@gmail.com"
                        recipient_list = ['ivishalthapa21@gmail.com']  # Replace with the actual admin email
                        
                        send_mail(subject, plain_message, from_email, recipient_list,html_message=html_message, fail_silently=False)
                        messages.success(request, f"{first_name}, your registration as an instructor is pending approval.")
                    else:
                        # Automatically set the role to student and register
                        Profile.objects.create(user=user, role='student', is_approved=True)
                        messages.success(request, 'User registered successfully.')

                    return redirect('login')
            else:
                messages.error(request, "Passwords do not match")
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
        
        return redirect('register')
   

# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'accounts/register.html')

#     def post(self, request):
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password1 = request.POST.get('password1')
#         role = request.POST.get('role')  # Get the role from the form
        
#         # Validate roles
#         valid_roles = ['admin', 'instructor', 'student']
#         if role not in valid_roles:
#             messages.error(request, "Invalid role selected.")
#             return redirect('register')

#         try:
#             if username.lower() in password.lower():
#                 messages.error(request, "Your password is too similar to username")
#                 return redirect('register')
            
#             if not re.search(r"[A-Z]", password):
#                 messages.error(request, "Your password must contain at least one uppercase letter")
#                 return redirect('register')

#             if not re.search(r"\d", password):
#                 messages.error(request, "Your password must contain at least one digit")
#                 return redirect('register')

#             validate_password(password)
#             if password == password1:
#                 if User.objects.filter(username=username).exists():
#                     messages.error(request, "Username already exists")
#                 elif User.objects.filter(email=email).exists():
#                     messages.error(request, 'Email already exists')
#                 else:
#                     user = User.objects.create_user(
#                         first_name=first_name, 
#                         last_name=last_name, 
#                         username=username, 
#                         email=email, 
#                         password=password
#                     )
                    
#                 # Set role to 'student' by default and send email if role is 'admin'
#                 # if role == 'admin':
#                     # Check if there is already an admin
#                     if role in ['admin', 'instructor']:
#                         if Profile.objects.filter(role='admin', is_approved=True).exists() or role == 'instructor':
#                             # Send email to the admin for approval
#                             subject = f"New {role.capitalize()} Registration - Approval Required"
#                             message = render_to_string('accounts/email_approval.html', {
#                                 'user': user,
#                                 'role': role.capitalize(),
#                                 'date': timezone.now(),
#                             })
#                             from_email = "ivishalthapa21@gmail.com"
#                         # recipient_list = ['admin@gmail.com']  # Replace with the actual admin email
#                             recipient_list = ['ivishalthapa21@gmail.com'] 
                            
#                             send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#                             messages.success(request, f"{first_name}, your registration as an {role} is pending approval.")
#                         else:
#                             # First admin registration does not need approval
#                             Profile.objects.create(user=user, role=role, is_approved=True)
#                             messages.success(request, 'User registered successfully.')
#                     else:
#                         # Automatically set the role to student and register
#                         Profile.objects.create(user=user, role='student', is_approved=True)
#                         messages.success(request, 'User registered successfully.')

#                     return redirect('login')
#             else:
#                 messages.error(request, "Passwords do not match")
#         except ValidationError as e:
#             for error in e.messages:
#                 messages.error(request, error)
        
#         return redirect('register')

    
# @login_required
class AdminDashboardView(View):
    def get(self, request):
        if request.user.profile.role != 'admin':
            return redirect('login')

        pending_profiles = Profile.objects.filter(is_approved=False).exclude(role='student')
        return render(request, 'accounts/admin_dashboard.html', {'pending_profiles': pending_profiles})
    

class ProfileApprovalView(View):
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        if request.user.profile.role == 'admin':
            profile.is_approved = True
            profile.save()
            messages.success(request, f"{profile.user.username} has been approved.")
        return redirect('admin_dashboard')
    

class ProfileApprovalView(View):
    def post(self, request, user_id, action):
        profile = get_object_or_404(Profile, user__id=user_id)
        user_role = request.user.profile.role
        # if request.user.profile.role == 'admin':
        if user_role in ['admin', 'instructor']:  # Allow both admin and instructor to approve/reject
            if action == 'approve':
                profile.is_approved = True
                profile.save()
                messages.success(request, f"Profile for {profile.user.username} has been approved.")
            elif action == 'reject':
                profile.user.delete()
                messages.success(request, f"Profile for {profile.user.username} has been rejected and deleted.")
            else:
                messages.error(request, "Invalid action.")
        else:
            messages.error(request, "You are not authorized to perform this action.")
        return redirect('admin_dashboard')
    

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the value of "Remember Me"
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            profile = Profile.objects.get(user=user)
            if profile.is_approved or profile.role == 'student':
                login(request, user)
                
                # Set session expiration based on the "Remember Me" checkbox
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser session ends
                    
                    
                # pass the role to the session or context
                request.session['role'] = profile.role
                #print(f"Role stored in session: {request.session['role']}")
                
                # Redirect based on role
                if profile.role == 'admin':
                    return redirect('admin_dashboard')  # Replace with your admin dashboard URL name
                elif profile.role == 'instructor':
                    return redirect('home')  # Replace with your instructor dashboard URL name
                else:
                    return redirect('home')  # Redirect students to course list
                
            else:
                messages.error(request, "Your account is pending approval.")
                return redirect('login')
        
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

from django.utils.decorators import method_decorator
@method_decorator(login_required(login_url='login'), name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)
        context = {
            'profile_form': profile_form,
            'user': request.user,
            'profile': request.user.profile,
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect("profile")
        else:
            context = {
                'profile_form': profile_form,
                'user': request.user,
                'profile': request.user.profile,
            }
            return render(request, 'accounts/profile.html', context)
        
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class ApproveUsersView(View):
    def get(self, request):
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to view this page.")
            return redirect('home')

        pending_profiles = Profile.objects.filter(is_approved=False, role__in=['admin', 'instructor'])
        # return render(request, 'accounts/approve_users.html', {'pending_profiles': pending_profiles})
        return render(request, 'accounts/admin_approval.html', {'pending_profiles': pending_profiles})
    

    def post(self, request):
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('home')

        profile_id = request.POST.get('profile_id')
        profile = Profile.objects.get(id=profile_id)
        profile.is_approved = True
        profile.save()
        messages.success(request, f'User {profile.user.username} has been approved.')
        return redirect('approve_users')

'''
class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        role = request.POST.get('role')  # Get role from form

        valid_roles = ['admin', 'instructor', 'student']
        if role not in valid_roles:
            messages.error(request, "Invalid role selected")
            return redirect('register')

        # Additional validations and password checks...
        try:
            validate_password(password)
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    profile = Profile.objects.create(user=user, role='student')  # Default role as student

                    if role != 'student':
                        # Send email to admin for approval
                        subject = "New User Registration - Approval Required"
                        message = render_to_string('accounts/email_approval.html', {
                        'user': user,
                        'date': timezone.now(),
                    })
                        from_email = "ivishalthapa21@gmail.com"
                        recipient_list = ['admin@example.com']  # Replace with the actual admin email
                    
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                        messages.success(request, f"{first_name}, your registration is successful. An admin will review your account shortly.")
                        # return redirect('login')
                        messages.success(request, 'Registration successful! Awaiting admin approval.')
                    else:
                        messages.success(request, 'Registration successful!')
                    
                    return redirect('login')
            else:
                messages.error(request, "Passwords do not match")
                return redirect('register')
        
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)

        return redirect('register')


'''

# ########################################################
#                   FUNCTION BASED VIEWS
# ########################################################


'''
# to display user first name and profile picture in navbar
def home(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
    
    return render(request, 'home.html', {'profile': profile})


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        role = request.POST.get('role')
        
        # validate roles
        valid_roles = ['admin', 'instructor', 'student']
        if role not in valid_roles:
            messages.error(request, "Invalid role selected.")
            return redirect('register')
        
        try:
            if username.lower() in password.lower():
                messages.error(request, "Username and password cannot be the same.")
                return redirect('register')
            
            # password validation uppercase
            if not re.search("[A-Z]", password):
                messages.error(request, "Password must contain at least one uppercase letter.")
                return redirect('register')
            
            # password validation to check atleast one number
            if not re.search(r"\d", password):
                messages.error(request, "Password must contain at least one number.")
                return redirect('register')
            
            validate_password(password)
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                    
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists.")
                    
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    Profile.objects.create(user=user, role=role)    # Create profile with role
                    messages.success(request, 'User created')
                    return redirect('login')
                
            else:
                messages.error(request, "Passwords do not match")
                return redirect('register')
            
            
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
                
    return render(request, 'accounts/register.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Username does not exist.")
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Get the user's role
            user_profile = Profile.objects.get(user=user)
            print(user_profile)
            user_role = user_profile.role
            print(user_role)
            
            # Redirect based on role
            if user_role == "admin":
                return redirect('admin_dashboard')
            elif user_role == "instructor":
                return redirect('instructor_dashboard')
            else:
                return redirect('student_dashboard')
            
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    
    return render(request, 'accounts/login.html')

@login_required(login_url = "login")
def log_out(request):
    logout(request)
    return redirect('login')


@login_required(login_url = "login")
def profile(request):
    profile = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=profile)
    
    if request.method =="POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect("profile")
        
    context = {
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'accounts/profile.html', context)

# @login_required(login_url = "login")
# def admin_dashboard(request):
#     return render(request, 'dashboards/admin_dashboard.html')


# @login_required(login_url = "login")
# def instructor_dashboard(request):
#     return render(request, 'dashboards/instructor_dashboard.html')


# @login_required(login_url = "login")
# def student_dashboard(request):
#     return render(request, 'dashboards/student_dashboard.html')


'''