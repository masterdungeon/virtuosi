from django.urls import path
from django.urls import include, re_path
from . import views

from .views import IndexView, ListView, UploadDocumentView, DeleteView, RulesView


urlpatterns = [
    path('', (IndexView.as_view()), name='index'),
    path('list/', (ListView.as_view()), name='list'),
    path('upload/', (UploadDocumentView.as_view()), name='upload'),
    path('delete/<int:pk>/', (DeleteView.as_view()), name='delete'),
    path('rules/', (RulesView.as_view()), name='rules'),
]

