from django.db import models
from django.contrib.auth.models import User

class Suggestion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    REACTION_CHOICES = (
        ('like', '추천'),
        ('dislike', '싫어요'),
    )
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=REACTION_CHOICES)

class SuggestionReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True: 추천, False: 비추천

    class Meta:
        unique_together = ('user', 'suggestion')

