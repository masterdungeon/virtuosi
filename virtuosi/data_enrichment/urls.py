from django.urls import path
from django.urls import include, re_path
from . import views

from .views import (
    IndexView,
    ListView,
    UploadDocumentView,
    DeleteView,
    RulesView,
    TemplateView,
    RuleRunView,
    DownloadView,
)

urlpatterns = [
    path("", (IndexView.as_view()), name="index"),
    path("list/", (ListView.as_view()), name="list"),
    path("upload/", (UploadDocumentView.as_view()), name="upload"),
    path("delete/<int:pk>/", (DeleteView.as_view()), name="delete"),
    path("rules/", (RulesView.as_view()), name="rules"),
    path("rule_run/<int:pk>/", (RuleRunView.as_view()), name="rule_run"),
    path("template/", (TemplateView.as_view()), name="template"),
    path("download/", (DownloadView.as_view()), name="download"),
]
