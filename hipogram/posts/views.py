from itertools import count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from hipogram.posts.forms import EditForm, PostForm
from hipogram.posts.models import Post
from django.core.paginator import Paginator

def post_list_view(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by("-creation_datetime")
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "post_list.html", {'posts': page_obj})
    

#Create post creation page
def post_create_view(request):
    if request.user.is_authenticated:
        form = PostForm()
        if request.method == 'POST': 
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.created_by = request.user
                new_post.save()
                form.save_m2m()
                return HttpResponseRedirect('/')
        return render(request, 'post_create.html', context={'form': form})

#Tag list view
def tag_list_view(request, tag):
    if request.method == 'GET':
        posts = Post.objects.filter(tags__slug=tag).order_by("-creation_datetime")
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "post_list.html", {'posts': page_obj})

#Post edit view
def post_edit_view(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=pk)
        form = EditForm(instance=post)
        if request.method == 'POST' and request.user == post.created_by: 
            form = EditForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.save()
                form.save_m2m()
                return HttpResponseRedirect('/')
        return render(request, 'post_edit.html', context={'form': form,'post':post})

