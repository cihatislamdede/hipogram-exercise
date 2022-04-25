from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from hipogram.posts.forms import EditForm, PostForm
from hipogram.posts.models import Post
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count 

def post_list_view(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by("-creation_datetime")
        return post_render_view(request, posts)

#Create post view
@login_required
def post_create_view(request):
    form = PostForm()
    if request.method == 'POST': 
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.save()
            #for tags 
            form.save_m2m()
            return HttpResponseRedirect('/')
    return render(request, 'post_create.html', context={'form': form})

#Post edit view
@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post,pk=pk)
    form = EditForm(instance=post)
    if request.user == post.created_by: 
        if 'edit' in request.POST:
            form = EditForm(request.POST, instance=post)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.save()
                #for tags
                form.save_m2m()
                return HttpResponseRedirect('/')
        elif 'delete' in request.POST:
            post.delete()
            return HttpResponseRedirect('/')
        return render(request, 'post_edit.html', context={'form': form,'post_image_url':post.image.url})
    else:
        return HttpResponseRedirect('/')

#Post of tags list view
def tag_list_view(request, tag):
    if request.method == 'GET':
        posts = Post.objects.filter(tags__slug=tag).order_by("-creation_datetime")
        return post_render_view(request, posts)

#Posts of user list view
def user_posts_view(request, userName):
    if request.method == 'GET':
        posts = Post.objects.filter(created_by__username=userName).order_by("-creation_datetime")
        return post_render_view(request, posts)

#Post render view
def post_render_view(request,posts):
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "post_list.html", {'posts': page_obj, 'tags': today_trend_tags()})

#Trend tags shared today (top 5 tags)
def today_trend_tags():
    today = datetime.today().date()
    return Post.objects.filter(creation_datetime__date__gte=today).exclude(tags=None).values('tags__name','tags__slug').annotate(count=Count('tags__name')).order_by('-count')[:5]

#Like post view
@login_required
def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=pk)
        if 'unlike' in request.POST:
            post.likes.remove(request.user)
        elif 'like' in request.POST:    
            post.likes.add(request.user)
        return HttpResponseRedirect('/')

#Search box by description text
def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('search',None)
        if query:
            return post_render_view(request, Post.objects.filter(text__icontains=query))
        else:
            return HttpResponseRedirect('/')

#Top all time 5 posts according to likes
def top_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by("-likes")[:5]
        return post_render_view(request, posts)
