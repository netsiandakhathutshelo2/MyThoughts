from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, ThoughtForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Thought


# Create your views here.
def homepage(request):

    return render(request, 'journal/index.html')


# Create your views here.
def register(request):
    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'user created')
            return redirect('my-login')

    context = {'RegistrationForm': form}

    return render(request, 'journal/register.html', context)


# Create your views here.
def my_login(request):

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'LoginForm': form}

    return render(request, 'journal/mylogin.html', context)


def user_logout(request):
    auth.logout(request)
    return redirect('')


# Create your views here.
@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'journal/dashboard.html')


@login_required(login_url='my-login')
def create_thought(request):
    form = ThoughtForm()

    if request.method == "POST":
        form = ThoughtForm(request.POST)

        if form.is_valid():
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            return redirect('my-thought')

    context = {'CreateThoughtForm': form}
    return render(request, 'journal/create-thought.html', context)


@login_required(login_url='my-login')
def my_thought(request):
    current_user = request.user.id
    thought = Thought.objects.all().filter(user=current_user)

    context = {'AllThoughts': thought}
    return render(request, 'journal/my-thought.html', context)


@login_required(login_url='my-login')
def update_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)

    except:
        return redirect('my-thought')

    form = ThoughtForm(instance=thought)
    if request.method == "POST":
        form = ThoughtForm(request.POST, instance=thought)

        if form.is_valid():
            form.save()

            return redirect('my-thought')

    context = {'UpdateThoughts': form}
    return render(request, 'journal/update-thought.html', context)


@login_required(login_url='my-login')
def delete_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)

    except:

        return redirect('my-thought')

    if request.method == "POST":
        thought.delete()
        return redirect('my-thought')

    return render(request, 'journal/delete-thought.html')

