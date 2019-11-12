from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout


def register_page(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")

            # if the request is a post request that meets validation then save users data.
    else:  # this means it is a GET request.
        form = UserCreationForm()
    return render(request, "accounts/register.html", {'form': form})


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect("/")
            # login in the user
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {'form': form})


def logout_page(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect("/")
