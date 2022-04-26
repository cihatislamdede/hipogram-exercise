from django import forms
from .models import Post


#Share post form
class PostForm(forms.ModelForm):
    #required image and text
    class Meta:
        model = Post
        fields = ['image', 'text', 'tags']

#Edit post form
class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'tags']
