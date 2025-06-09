from django.db import models
from django.contrib.auth.models import User

class UsedBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)  # 이미지 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
