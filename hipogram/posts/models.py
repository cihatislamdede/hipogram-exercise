from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=35)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

class Post(models.Model):
    image = models.ImageField()
    text = models.TextField(blank=True)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag,related_name='posts', blank=True)
    likes = models.ManyToManyField("auth.User", related_name='likes', blank=True)
    comments = models.ManyToManyField(Comment, related_name='posts', blank=True)

    #Get tags
    def get_tags(self):
        return self.tags.all()
    
    def __str__(self):
        return self.text[:30] or  "..."
