from django.db.models import Avg

from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NoteSerializer, NoteDetailSerializer, NoteEditorSerializer, CommentAddSerializer, CommentSerializer

from .models import Note, Comment


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
        notes = Note.objects.all().order_by('-date_add', 'title')
        notes_serializer = NoteSerializer(notes, many=True)
        return Response(notes_serializer.data)


class NoteDetailView(APIView):
    """Получить 1 статью"""
    def get(self, request, note_id):
        note = Note.objects.filter(pk=note_id, public=True).first()

        if not note:
            raise NotFound(f'Опубликованная статья с id={note_id} не найдена')

        serializer = NoteDetailSerializer(note)
        return Response(serializer.data)


class NoteEditorView(APIView):
    """ Добавление или изменение статьи """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ Новая статья для блога """
        # Передаем в сериалайзер (валидатор) данные из запроса
        new_note = NoteEditorSerializer(data=request.data)
        # Проверка параметров
        if new_note.is_valid():
            # Записываем новую статью и добавляем текущего пользователя как автора
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, note_id):
        # Находим редактируемую статью
        note = Note.objects.filter(pk=note_id, author=request.user).first()
        if not note:
            raise NotFound(f'Статья с id={note_id} для пользователя {request.user.username} не найдена')

        new_note = NoteEditorSerializer(note, data=request.data, partial=True)

        if new_note.is_valid():
            new_note.save()
            return Response(new_note.data, status=status.HTTP_200_OK)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    """ Комментарий к статье """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """ Получить список всех комментов """
        comments = Comment.objects.all().order_by('-date_add', 'note')
        comments_serializer = CommentSerializer(comments, many=True)
        return Response(comments_serializer.data)

    def post(self, request, note_id):
        """ Новый комментарий """

        note = Note.objects.filter(pk=note_id).first()
        if not note:
            raise NotFound(f'Статья с id={note_id} не найдена')

        new_comment = CommentAddSerializer(data=request.data)
        if new_comment.is_valid():
            new_comment.save(note=note, author=request.user)
            return Response(new_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """ Удалить комментарий """
        comment = Comment.objects.filter(pk=comment_id, author=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
