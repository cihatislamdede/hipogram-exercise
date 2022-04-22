from django.http import HttpResponseRedirect
from django.shortcuts import render
from hipogram.posts.forms import PostForm
from hipogram.posts.models import Post
from django.core.paginator import Paginator

def post_list_view(request):
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
