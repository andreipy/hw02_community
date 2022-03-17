from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Group, Post, User


@login_required
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    all_authors_posts = Post.objects.select_related('author').all()
    post_count = 0
    for post in all_authors_posts:
        if post.author.username == username:
            post_count += 1
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'author': author
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    all_authors_posts = Post.objects.select_related('author').all()
    post_count = 0
    for post in all_authors_posts:
        if post.id == post_id:
            author_of_post = post.author.username
    for post in all_authors_posts:
        if post.author.username == author_of_post:
            post_count += 1
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post_count': post_count,
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)
