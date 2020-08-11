from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .models import Post
from .forms import PostForm, AuthUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context = {
            'posts': posts,
    }
    return render(request, 'blog/post_list.html',context) 


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
            'post': post,
    }
    return render(request, 'blog/post_detail.html', context)

def post_edit(request, pk):
    if request.method == "POST":
        form = PostForm()
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(reverse('post_detail', pk=post.pk))
    else:
        form = PostForm()
        post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_edit.html', {'form': form, 'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(reverse('blog:post_detail', kwargs={'pk':post.pk}))
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect(reverse('blog:post_list'))

