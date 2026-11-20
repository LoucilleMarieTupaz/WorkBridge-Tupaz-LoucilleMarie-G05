from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistrationForm


def register_view(request):
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