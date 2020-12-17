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
    DownloadView,
)

urlpatterns = [
    path("", (IndexView.as_view()), name="index"),
    path("list/", (ListView.as_view()), name="list"),
    path("upload/", (UploadDocumentView.as_view()), name="upload"),
    path("delete/<int:pk>/", (DeleteView.as_view()), name="delete"),
    path("rules/", views.rules, name="rules"),
    path("rules/new/", views.rule_create, name='rule_create'),
    path("rules/edit/<int:pk>/" , views.rule_update, name='rule_edit'),
    path("rules/delete/<int:pk>/", views.rule_delete, name='rule_delete'),
    path("rule_run/<int:pk>/", views.rule_run, name="rule_run"),
    path("template/", (TemplateView.as_view()), name="template"),
    path("download/", (DownloadView.as_view()), name="download"),
    path("save_rule/" , views.save_rule, name='save_rule'),
    path("save_rule_condition/" , views.save_rule_condition, name='save_rule_condition'),
]
