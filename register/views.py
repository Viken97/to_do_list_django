from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

def register(request):
    """
    View for registering a new user.

    Parameters:
    - request: HttpRequest object

    Returns:
    - Rendered HTML template displaying the home page of the new user
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Log in the user
            login(request, user)

            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})
