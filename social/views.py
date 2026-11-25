from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'social/register.html', {'form': form})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    users = User.objects.exclude(id=request.user.id) if request.user.is_authenticated else User.objects.all()
    current_profile = None

    if request.user.is_authenticated:
        current_profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(user=request.user, content=content)
        return redirect('post_list')

    context = {
        'posts': posts,
        'users': users,
        'current_profile': current_profile,
    }
    return render(request, 'social/post_list.html', context)


@login_required(login_url='/admin/login/')
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_list')


@login_required(login_url='/admin/login/')
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Comment.objects.create(post=post, user=request.user, body=body)
    return redirect('post_list')


@login_required(login_url='/admin/login/')
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if target_user != request.user:
        if target_user in profile.following.all():
            profile.following.remove(target_user)
        else:
            profile.following.add(target_user)
    return redirect('post_list')


def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=target_user)
    user_posts = Post.objects.filter(user=target_user).order_by('-created_at')
    return render(request, 'social/profile.html', {
        'target_user': target_user,
        'profile': profile,
        'posts': user_posts,
    })
