from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import Post
from django.contrib.auth.decorators import login_required


def mypage(request, id):
    user=get_object_or_404(User, pk=id)
    user_posts = Post.objects.filter(author=user)
    context = {
        'user':user,
        'posts': user_posts
    }
    return render(request,'users/mypage.html', context)

def follow(request,id):
    user = request.user
    followed_user = get_object_or_404(User, pk=id)
    is_follower=user.profile in followed_user.profile.followers.all()
    if is_follower:
        user.profile.followings.remove(followed_user.profile)
    else:
        user.profile.followings.add(followed_user.profile)
    return redirect('users:mypage', followed_user.id)

    