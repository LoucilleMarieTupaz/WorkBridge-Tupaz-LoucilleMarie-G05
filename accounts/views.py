from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Your WorkBridge account has been created successfully!'
            )

            return redirect('accounts:dashboard')

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                'You have successfully logged in to WorkBridge!'
            )

            return redirect('accounts:dashboard')

        else:
            messages.error(
                request,
                'Invalid username or password. Please try again.'
            )

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(
            request,
            'You have successfully logged out.'
        )
        return redirect('accounts:login')

    return redirect('accounts:login')

@login_required
def dashboard_view(request):

    user = request.user

    if user.role == 'ADMIN':
        return redirect('accounts:admin_dashboard')

    elif user.role == 'PROJECT_MANAGER':
        return redirect('accounts:manager_dashboard')

    else:
        return redirect('accounts:member_dashboard')


@login_required
def admin_dashboard(request):

    if request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/admin_dashboard.html')


@login_required
def manager_dashboard(request):

    if request.user.role != 'PROJECT_MANAGER':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/manager_dashboard.html')


@login_required
def member_dashboard(request):

    if request.user.role != 'MEMBER':
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/member_dashboard.html')

@login_required
def profile_view(request):

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('accounts:profile')

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request,
        'accounts/profile.html',
        {'form': form}
    )

def home_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    return redirect('accounts:login')