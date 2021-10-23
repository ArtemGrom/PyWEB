from django.urls import path
from .views import NoteView


app_name = "blog"
urlpatterns = [
    path('', NoteView.as_view()),
]
