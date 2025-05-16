from django.urls import path
from .views import CVListView, CVDetailView, download_pdf, SettingsView

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", download_pdf, name="cv_pdf"),
    path("settings/", SettingsView.as_view(), name="settings"),
]