from django.urls import path

from .views import NoteView, NoteDetailView, NoteEditorView, CommentDetailView


app_name = "blog"
urlpatterns = [
    path('notes/', NoteView.as_view(), name='notes'),
    path('notes/<int:note_id>/', NoteDetailView.as_view(), name='note'),
    path('notes/add/', NoteEditorView.as_view(), name='add'),
    path('notes/<int:note_id>/save/', NoteEditorView.as_view(), name='save'),

    path('comment/', CommentDetailView.as_view(), name='comment_display'),
    path('comment/<int:note_id>/add/', CommentDetailView.as_view(), name='comment_add'),
    path('comment/<int:comment_id>/del/', CommentDetailView.as_view(), name='comment_del'),
]
