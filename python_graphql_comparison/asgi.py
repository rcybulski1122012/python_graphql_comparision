"""
ASGI config for python_graphql_comparison project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

import ariadne.asgi
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path, re_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_graphql_comparison.settings")
django_application = get_asgi_application()

from python_graphql_comparison.graphql.ariadne.schema import schema  # noqa: E402

ariadne_application = ariadne.asgi.GraphQL(schema)

application = URLRouter(
    [
        path("ariadne/graphql/", ariadne_application),
        re_path(r"^", django_application),
    ]
)
