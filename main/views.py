from  django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import *
# Create your views here.

def mainpage(request):
    return render(request, 'main/mainpage.html')

def secondpage(request):
    posts = Post.objects.all()
    return render(request, 'main/secondpage.html', {'posts': posts})

def new_post(request):
    return render(request, 'main/new-post.html')

def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        return render(request, 'main/detail.html', {'post' : post, 'comments' : comments})

    elif request.method == 'POST':
        new_comment = Comment()
        new_comment.post = post
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()
        return redirect('main:detail',id)

def create(request):
    if request.user.is_authenticated:
        new_post = Post()

        new_post.title = request.POST['title']
        new_post.writer = request.user
        new_post.author = request.user
        new_post.weather = request.POST['weather']
        new_post.content = request.POST['content']
        new_post.pub_date = timezone.now()
        new_post.image = request.FILES.get('image')

        new_post.save()

    # 본문을 띄어쓰기 기준으로 나눔
        words = new_post.content.replace('\n', ' ').split(' ')
        tag_list = []

    # 나눈 단어가 '#'으로 시작한다면 tag_list에 저장
        for w in words:
            if len(w) > 0:
                if w[0] == '#':
                    tag_list.append(w[1:])  # '#' 제외하고 단어만 추가

    # tag_list에 있는 Tag들을 new_blog의 tags에 추가
        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            new_post.tags.add(tag.id)

        return redirect('main:detail', new_post.id)
    else:
        return redirect('accounts:login')
    
def edit(request, id) :
    edit_post = Post.objects.get(pk=id)
    return render(request, 'main/edit.html', {"post":edit_post})

def update(request, id):
    update_post = get_object_or_404(Post, pk=id)

    if request.user.is_authenticated and request.user == update_post.writer:
        update_post.title = request.POST['title']
        update_post.weather = request.POST['weather']
        update_post.content = request.POST['content']
        update_post.pub_date = timezone.now()

        if request.FILES.get('image'):
            update_post.image = request.FILES.get('image')

        update_post.save()

        
        update_post.tags.clear()

        
        words = update_post.content.replace('\n', ' ').split(' ')
        tag_list = []

        for w in words:
            if len(w) > 0 and w[0] == '#':
                tag_list.append(w[1:])  

        for t in tag_list:
            tag, _ = Tag.objects.get_or_create(name=t)
            update_post.tags.add(tag)

        return redirect('main:detail', update_post.id)

    return redirect('accounts:login')

def delete(request, id):
    delete_post = Post.objects.get(pk=id)
    delete_post.delete()
    return redirect('main:secondpage')

def tag_list(request): #모든 태그 목록을 볼 수 있는 페이지
    tags = Tag.objects.all()
    return render(request, 'main/tag-list.html', {'tags': tags})

def tag_posts(request, tag_id): #특정 태그를 가진 게시글의 목록을 볼 수 있는 페이지
    tag=get_object_or_404(Tag, id=tag_id)
    posts=tag.posts.all()
    return render(request, 'main/tag-post.html', {
        'tag' : tag,
        'posts' : posts
    })

def likes(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count += 1
        post.save()
    return redirect('main:detail', post_id)

