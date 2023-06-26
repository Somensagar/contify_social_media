from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Friend, Post
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q


def user_login(request):
    if request.method == "GET":
        return render(request, 'loginpage.html')
    else:
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request, 'Login Successfully')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid Username and Password')
            return redirect('user_login')


def user_register(request):
    if request.method == 'GET':
        return render(request, 'registerpage.html')
    else:
        username = request.POST.get('user')
        password = request.POST.get('password')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_pic')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Same Username already exists.')
            return render(request, 'registerpage.html')
        new_user = User.objects.create(username=username)
        new_user.set_password(password)
        new_user.save()

        profile = UserProfile.objects.create(
            user=new_user,
            age=age,
            gender=gender,
            dob=dob,
            profile_pic = profile_pic
        )
        profile.save()
        return redirect('successfullyregister')


def profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    if request.method == "GET":
        return render(request, 'profile.html', {'userprofile': user_profile})


def update_profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    if request.method == "GET":
        return render(request, 'updateprofile.html', {'userprofile': user_profile})
    else:
        user = User.objects.get(username=username)
        new_username = request.POST.get('user')
        if user.username != new_username:
            user.username = new_username
        user.save()
        user_profile.user = user
        user_profile.age = request.POST.get('age')
        user_profile.gender = request.POST.get('gender')
        user_profile.dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            user_profile.profile_pic = profile_pic
        user_profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile', username=new_username)


def successfullyregister(request):
    messages.success(request, 'Successfully Register Your Infromation')
    return render(request, 'successfullyregister.html')


def user_logout(request):
    logout(request)
    messages.error(request, 'Logout Successfully')
    return redirect('user_login')


def passwordupdated(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        user = authenticate(username=request.user.username, password=old_password)
        if user is not None:
            if new_password:
                user.set_password(new_password)
                user.save()
                logout(request)
                messages.success(request, 'Password updated successfully. Please login again.')
                return redirect('user_login')

        messages.error(request, 'Incorrect old password.')

    return render(request, 'passwordupdated.html')


def search_friends(request):
    query = request.GET.get('query')
    friends = []

    if query:
        friends = User.objects.filter(username__icontains=query).exclude(id=request.user.id).select_related('userprofile')

        for friend in friends:
            friend.userprofile.is_friend = Friend.objects.filter(user=request.user, friend=friend).exists()
            friend.userprofile.is_pending = Friend.objects.filter(user=friend, friend=request.user).exists()

    return render(request, 'search_friends.html', {'friends': friends, 'query': query})


def send_friend_request(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    friend_obj, created = Friend.objects.get_or_create(user=request.user, friend=friend)

    if created:
        messages.success(request, 'Friend request sent')
    elif friend_obj.status == 'pending':
        friend_obj.delete()
        messages.info(request, 'Friend request canceled')
    elif friend_obj.status == 'accepted':
        friend_obj.delete()  # Remove friend
        messages.info(request, 'Friend removed')
    else:
        friend_obj.status = 'pending'
        friend_obj.save()
        messages.success(request, 'Friend request sent')

    return redirect('search_friends')


def view_friend_requests(request):
    friend_requests = Friend.objects.filter(friend=request.user, status='pending').select_related('friend')
    return render(request, 'friend_requests.html', {'friend_requests': friend_requests})


def accept_friend_request(request, friend_id):
    try:
        friend_request = get_object_or_404(Friend, friend=request.user, user_id=friend_id, status='pending')
        friend_request.accept()
        Friend.objects.create(user=request.user, friend=friend_request.user, status='accepted')
        messages.success(request, 'Friend request accepted successfully.')
        return redirect('view_friends_list')
    except ObjectDoesNotExist:
        return HttpResponse("Friend request does not exist.")


def cancel_friend_request(request, friend_id):
    try:
        friend_request = Friend.objects.get(user=friend_id, friend=request.user, status='pending')
        friend_request.delete()
        messages.info(request, 'Friend request canceled')
    except Friend.DoesNotExist:
        messages.error(request, 'Friend request does not exist.')
    return redirect('view_friend_requests')


def remove_friend(request, friend_id):
    try:
        friend = Friend.objects.get(user=request.user, friend_id=friend_id)
        friend.delete()
        reverse_friend = Friend.objects.get(user=friend.friend, friend=request.user)
        reverse_friend.delete()
        messages.success(request, 'Friend removed successfully.')
    except Friend.DoesNotExist:
        pass
    return redirect('view_friends_list')


def view_friends_list(request):
    friends = Friend.objects.filter(user=request.user, status='accepted').select_related('friend').exclude(id=request.user.id)
    return render(request, 'friends_list.html', {'friends': friends})


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        user = request.user
        date_posted = datetime.now()
        post = Post(title=title, image=image, user=user, date_posted=date_posted)
        post.save()
        messages.success(request, 'Posted Successfully')
        return redirect('homepage')
    return render(request, 'post_create.html')


def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        if 'image' in request.FILES:
            post.image = request.FILES.get('image')
        post.save()
        messages.success(request, 'Update Post Successfully')
        return redirect('homepage')
    return render(request, 'post_update.html', {'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.error(request, 'Delete Post Successfully')
        return redirect('homepage')
    return redirect('homepage')


def homepage(request):
    user = request.user
    friends = user.friendships.filter(status='accepted').values_list('friend', flat=True)
    posts = Post.objects.filter(Q(user=user) | Q(user__in=friends)).order_by('-date_posted')
    posts_per_page = 2
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj,
    }
    return render(request, 'homepage.html', context)


def user_post_list(request):
    posts = Post.objects.filter(user=request.user).order_by('-date_posted')
    posts_per_page = 2
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj,
    }
    return render(request, 'user_post_list.html', context)



