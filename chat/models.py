from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participants_names = ", ".join([user.username for user in self.participants.all()])
        return f"ChatRoom({participants_names})"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at}] {self.sender.username}: {self.text}"
