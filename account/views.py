from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, EditProfileForm, PhoneLoginForm, VerifyCodeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.models import Post
from .models import Profile, Relation
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from django import forms
from django.http import JsonResponse


# Create your views here.

def user_login(request):
    next_url = request.GET.get('next', None)
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                if next_url:
                    return redirect(next_url)
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'Wrong Username or password', 'warning')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            messages.success(request, 'You registered successfully', 'success')
            return redirect('posts:all_posts')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You are logged out now', 'success')
    return redirect('posts:all_posts')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    self_dash = False
    is_fallowing = False
    relation = Relation.objects.filter(from_user=request.user, to_user=user)
    if relation.exists():
        is_fallowing = True
    if request.user.id == user_id:
        self_dash = True
    return render(request, 'account/dashboard.html',
                  {'user': user, 'posts': posts, 'self_dash': self_dash, 'is_following': is_fallowing})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Your profile edited successfully', 'success')
            return redirect('account:dashboard', user_id)
    else:
        form = EditProfileForm(instance=user.profile, initial={'email': request.user.email})

    return render(request, 'account/edit_profile.html', {'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            global phone, rand_num
            phone = f"0{form.cleaned_data['phone']}"
            rand_num = randint(1000, 9999)
            api = KavenegarAPI(
                '564541673171767A7436614B476E5173553367647A64696270362F2F794D6D7235416C496852794B4833633D')
            params = {'sender': '', 'receptor': phone, 'message': rand_num}
            api.sms_send(params)
            return redirect('account:verify', phone, rand_num)
    else:
        form = PhoneLoginForm()

    return render(request, 'account/phone_login.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if rand_num == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, phone=phone)
                user = get_object_or_404(User, profile__id=profile.id)
                login(request, user)
                messages.success(request, 'logged in successfully.')
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'Your code is wrong', 'error')
    else:
        form = VerifyCodeForm()

    return render(request, 'account/verify.html', {'form': form})


@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            Relation(from_user=request.user, to_user=following).save()
            return JsonResponse({'status': 'ok'})


@login_required
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not exists'})
