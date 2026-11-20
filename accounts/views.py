from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:login')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Your WorkBridge account has been created successfully!'
            )

            return render(
                request,
                'accounts/register_success.html',
                {'user': user}
            )

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

def login_view(request):
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

            return render(
                request,
                'accounts/login_success.html'
            )

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