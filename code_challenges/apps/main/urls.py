from django.urls import path

from code_challenges.apps.main.views import HomeView

app_name = "main"
urlpatterns = [
    path("", HomeView.as_view())
]
