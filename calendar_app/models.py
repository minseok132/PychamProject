from django.db import models

class WorkLog(models.Model):
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=6, decimal_places=4)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} – {self.hours_worked}h"


class Memo(models.Model):
    date = models.DateField()
    note = models.TextField()

    def __str__(self):
        return f"{self.date} – {self.note[:20]}…"


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} – {self.title}"


class CafeteriaMenu(models.Model):
    date = models.DateField(unique=True)
    menu_text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} 급식메뉴"


class MenuPhoto(models.Model):
    menu = models.ForeignKey(
        CafeteriaMenu,
        related_name='photos',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='lunch_menus/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Suggestion(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu.date} 사진 ({self.uploaded_at:%Y-%m-%d %H:%M})"


