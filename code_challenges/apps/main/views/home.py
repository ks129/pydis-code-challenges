from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Show page is not ready notice."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Show home page."""
        from datetime import datetime, timedelta, timezone
        context = {
            "challenge_end_time": (datetime.now() + timedelta(hours=20)).isoformat()
        }
        return render(request, "main/home.html", context)
