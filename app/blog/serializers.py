from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


class AuthorSerializer(serializers.ModelSerializer):
    """ Автор статьи """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class NoteSerializer(serializers.ModelSerializer):
    """Сериализует все статьи блога"""
    class Meta:
        """
        {
            "title": "Статья 1",
            "message": "Моя первая статья",
            "public": true
        }
        """
        model = Note
        fields = ['id', 'title', 'message', 'public', 'date_add']
        read_only_fields = ['date_add']


class NoteDetailSerializer(serializers.ModelSerializer):
    """Сериализует 1 статью блога """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"

    def to_representation(self, instance):
        """ Переопределение вывода. Меняем формат даты в ответе """
        ret = super().to_representation(instance)
        # Конвертируем строку в дату по формату
        date_add = datetime.strptime(ret['date_add'], '%Y-%m-%dT%H:%M:%S.%f') # Для даты с миллисекундами
        # date_add = datetime.strptime(ret['date_add'], '%Y-%m-%dT%H:%M:%S')
        # Конвертируем дату в строку в новом формате
        ret['date_add'] = date_add.strftime('%d %B %Y %H:%M:%S')
        return ret


class NoteEditorSerializer(serializers.ModelSerializer):
    """ Добавление или изменение статьи """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['date_add', 'author', ]