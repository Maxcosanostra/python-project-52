from django.urls import path
from .views_labels import (
    LabelListView,
    LabelCreateView,
    LabelUpdateView,
    LabelDeleteView,
)

urlpatterns = [
    path("labels/", LabelListView.as_view(), name="label_list"),
    path("labels/create/", LabelCreateView.as_view(), name="label_create"),
    path(
        "labels/<int:pk>/update/",
        LabelUpdateView.as_view(),
        name="label_update",
    ),
    path(
        "labels/<int:pk>/delete/",
        LabelDeleteView.as_view(),
        name="label_delete",
    ),
]
