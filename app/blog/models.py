from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    """Основная запись в приложении"""
    title = models.CharField(max_length=200)
    message = models.TextField()
    date_add = models.DateTimeField(auto_now=True)
    public = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=False)

    def __str__(self):
        """Возвращает строковое представление модели"""
        return self.title
