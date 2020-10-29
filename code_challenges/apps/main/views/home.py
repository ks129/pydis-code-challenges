from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    """Show page is not ready notice."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Show home page."""
        return HttpResponse((
            "Our page is not ready yet, "
            "but we hope to release this event as soon this is possible."
        ))
