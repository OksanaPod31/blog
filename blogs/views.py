from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Blog, BlogPost
from .forms import BlogForm, BlogPostForm
# Create your views here.


def index(request):
    """Домашняя страница приложения Blog"""
    return render(request, 'blogs/index.html')


@login_required
def blogs(request):
    """Выводит список тем."""
    blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)


@login_required
def blog(request, blog_id):
    """Выводит одну тему и все ее записи."""
    blog = Blog.objects.get(id=blog_id)
    if blog.owner != request.user:
        raise Http404
    posts = blog.blogpost_set.all()
    context = {'blog': blog, 'posts': posts}
    return render(request, 'blogs/blog.html', context)


@login_required
def new_blog(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = BlogForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:blogs')
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)


@login_required
def new_post(request, blog_id):
    """Добавляет новую запись по конкретной теме."""
    blog = Blog.objects.get(id=blog_id)
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = BlogPostForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id)
    # Вывести пустую или недействительную форму.
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """Редактирует существующую запись."""
    post = BlogPost.objects.get(id=post_id)
    blog = post.blog
    if blog.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = BlogPostForm(instance=post)
    else:
        # Отправка данных POST; обработать данные.
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)
    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'blogs/edit_post.html', context)
