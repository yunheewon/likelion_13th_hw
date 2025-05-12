from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import Post
from django.contrib.auth.decorators import login_required


def mypage(request, id):
    user=get_object_or_404(User, pk=id)
    user_posts = Post.objects.filter(writer=user.username)
    context = {
        'user':user,
        'posts': user_posts
    }
    return render(request,'users/mypage.html', context)
