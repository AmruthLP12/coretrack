from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.TrackerListView.as_view(), name="tracker-list"),
    path("create/", views.TrackerCreateView.as_view(), name="tracker-create"),
    path("update/<int:pk>/", views.TrackerUpdateView.as_view(), name="tracker-update"),
]