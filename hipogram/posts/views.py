from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from hipogram.posts.forms import EditForm, PostForm
from hipogram.posts.models import Post,Comment
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
    if request.method == 'POST': 
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.save()
            #for tags 
            form.save_m2m()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'post_create.html', context={'form': form})

#Post edit view
@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user == post.created_by:
        form = EditForm(instance=post)
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
    today = datetime.utcnow().date()
    trend_tags = Post.tags.through.objects.filter(post__creation_datetime__date = today).values('tag__name','tag__slug',).annotate(count=Count('tag__name')).order_by('-count')[:5]
    return trend_tags

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

#Top 5 posts according to likes (all time)
def top_posts(request):
    if request.method == 'GET':
        # like count > 0
        posts = Post.objects.annotate(like_count=Count('likes')).exclude(like_count=0).order_by('-like_count')[:5]
        return post_render_view(request, posts)

#Add comment to post
@login_required
def add_comment_to_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=pk)
        comment = request.POST.get('comment', None)
        if comment:
            new_comment = post.comments.create(text=comment, created_by=request.user)
            new_comment.save()
        return HttpResponseRedirect('/')

#Delete comment
@login_required
def delete_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment,pk=pk)
        if comment.created_by == request.user:
            comment.delete()
        return HttpResponseRedirect('/')