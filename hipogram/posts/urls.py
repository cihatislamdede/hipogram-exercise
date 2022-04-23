from django.urls import path

from .views import *

app_name = "posts"

urlpatterns = [
    path("", post_list_view, name="list"),
    path("create/", post_create_view, name="create"),
    path("tag/<slug:tag>/", tag_list_view, name="tag_list"),
    path("user/<str:userName>/", user_posts_view, name="user_posts"),
    path("edit/<int:pk>/", post_edit_view, name="edit"),
]
