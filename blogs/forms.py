from django import forms
from .models import Blog, BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name']
        labels = {'name': ''}


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost

        fields = ['title', 'text', 'date_added']
        labels = {'title': 'Title', 'text': 'Text', 'date_added': 'Date Added'}
        widgets = {'text': forms.Textarea(
            attrs={'cols': 80}), 'date_added': forms.DateInput(attrs={'type': 'date'})}
