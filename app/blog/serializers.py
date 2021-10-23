from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
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
