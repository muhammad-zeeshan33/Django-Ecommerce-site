from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User
from datetime import datetime
class Blog(models.Model):
    image = models.ImageField(upload_to='blogimages/', null=True)
    title =  models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    body = models.TextField()    
    published = models.BooleanField(default=True)
    created =  models.DateTimeField(default=datetime.now(), null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 

    @property
    def get_comments(self):
        items = self.comment_set.all().count()
        


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=DO_NOTHING, null=False, blank=False)
    comment = models.TextField(blank=False)
    commented_at = models.DateTimeField(auto_now=True)
    
    