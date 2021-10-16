from django.shortcuts import render
from .models import Note


def home(request):
    """Домашняя страница для приложения"""
    # Объект, который будет передан в шаблон
    context = {
        "message": "Добро пожаловать!!!",
        "left": "Это сообщение слева",
        "right": "Это сообщение справа",
    }

    return render(request, 'blog/index.html', context)
