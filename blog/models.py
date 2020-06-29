from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    nsfw = models.BooleanField(default=False)
    # on_delete = models.CASCADE tells django to delete a user's posts if the user is deleted

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # redirects to the post-detail url once a new post is created
        return reverse('post-detail', kwargs={'pk': self.pk})
