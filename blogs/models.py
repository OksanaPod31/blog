from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Blog(models.Model):
    """Blog model."""
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a human readable representation of the model object."""
        return self.name


class BlogPost(models.Model):
    """Blog post model."""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    title = models.CharField(max_length=500)
    text = models.TextField()
    date_added = models.DateField(auto_now_add=False)

    def __str__(self):
        """Return a string representing the blog post."""
        return f"{self.title[:50]}..."
