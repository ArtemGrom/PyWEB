from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NoteSerializer

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


class NoteView(APIView):
    def get(self, request):
        """ Получить список всех записей """
        notes = Note.objects.all()
        notes_serializer = NoteSerializer(notes, many=True)
        return Response(notes_serializer.data)
