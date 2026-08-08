from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Account created successfully!")

        return redirect('/')

    return render(request, 'register.html') 
def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request, "Login Successful!")

            return redirect('/')

        else:

            messages.error(request, "Invalid Username or Password")

            return redirect('login')

    return render(request, 'login.html')
def logout_user(request):

    logout(request)

    messages.success(request, "Logged out successfully!")

    return redirect('home')
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):

    from dashboard.models import Career
    from resumes.models import Resume

    career = Career.objects.filter(
        user=request.user
    ).first()

    resume = Resume.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "accounts/profile.html",
        {
            "career": career,
            "resume": resume,
        }
    )


@login_required
def edit_profile(request):

    # Create a profile if it doesn't already exist
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

     user_form = UserUpdateForm(
        request.POST,
        instance=request.user
    )

    profile_form = ProfileUpdateForm(
        request.POST,
        request.FILES,
        instance=profile
    )

    print("FILES:", request.FILES)

    if user_form.is_valid():
        print("User form valid")
    else:
        print(user_form.errors)

    if profile_form.is_valid():
        print("Profile form valid")
    else:
        print(profile_form.errors)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        print("Saved successfully")
        return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=profile
        )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(
        request,
        "accounts/edit_profile.html",
        context
    )