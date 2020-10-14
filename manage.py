#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import re
import socket
import sys
import time
import typing as t

import django
from django.contrib.auth import get_user_model
from django.core.management import call_command

log = logging.getLogger(__name__)

DEFAULT_ENVS = {
    "DJANGO_SETTINGS_MODULE": "code_challenges.settings",
    "SUPER_USERNAME": "admin",
    "SUPER_PASSWORD": "admin",
}

for key, value in DEFAULT_ENVS.items():
    os.environ.setdefault(key, value)


class SiteManager:
    """Manages preparation and serving of site."""

    def __init__(self, args: t.List[str]):
        self.debug = "--debug" in args

        if self.debug:
            os.environ.setdefault("DEBUG", "true")
            log.info("Starting in debug mode.")

    @staticmethod
    def create_superuser() -> None:
        """Create Django superuser for development environment."""
        log.info("Creating a superuser.")

        name = os.environ.get("SUPER_USERNAME")
        password = os.environ.get("SUPER_PASSWORD")
        user_model = get_user_model()

        if user_model.objects.filter(username=name).exists():
            log.info("Superuser already exists.")
        else:
            user_model.objects.create_superuser(name, '', password)
            log.info("Superuser created")

    @staticmethod
    def wait_for_postgres() -> None:
        """Wait for the main PostgreSQL database."""
        log.info("Waiting for PostgreSQL database.")

        # Get database URL based on environmental variable passed in compose
        database_url = os.environ["DATABASE_URL"]
        match = re.search(r"@([\w.]+):(\d+)/", database_url)
        if not match:
            raise OSError("Valid DATABASE_URL environmental variable not found.")
        domain = match.group(1)
        port = int(match.group(2))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        attempts_left = 10
        while attempts_left:
            try:
                s.connect((domain, port))
                s.shutdown(socket.SHUT_RDWR)
                log.info("Database is ready.")
                break
            except socket.error:
                attempts_left -= 1
                log.info("Database is not ready yet.")
                time.sleep(1)
        else:
            log.warning("Database could not be found, exiting.")
            sys.exit(1)

    def prepare_site(self) -> None:
        """Apply migrations and collect staticfiles."""
        django.setup()

        if self.debug:
            self.wait_for_postgres()

        log.info("Applying migrations...")
        call_command("migrate")
        log.info("Collecting staticfiles...")
        call_command("collectstatic", interactive=False, clear=True)

        if self.debug:
            self.create_superuser()

    def run(self) -> None:
        """Runs server with standard Django runner (dev) or with pyuwsgi (production)."""

        in_reloader = os.environ.get('RUN_MAIN') == 'true'

        # Prevent preparing twice when in dev mode due to reloader
        if not self.debug or in_reloader:
            self.prepare_site()

        log.info("Starting server...")

        # Development mode
        if self.debug:
            call_command("runserver", "0.0.0.0:8080")
            return

        # Production mode
        import pyuwsgi
        pyuwsgi.run(["--ini", "docker/uwsgi.ini"])


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_challenges.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        SiteManager(sys.argv).run()
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
