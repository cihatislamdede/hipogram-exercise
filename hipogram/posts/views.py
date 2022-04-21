from django.shortcuts import render
from hipogram.posts.models import Post

def post_list_view(request):
    posts = Post.objects.all().order_by("-creation_datetime")
    return render(request, "post_list.html", {'posts': posts})

#Create post creation page
def post_create_view(request):
    return render(request, 'post_create.html')
