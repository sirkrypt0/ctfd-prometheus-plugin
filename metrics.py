import logging
import os

from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from CTFd.utils import get_app_config

from .collector import MetricsCollector


logger = logging.getLogger("prometheus-metrics")


def load(app):
    logger.setLevel(get_app_config("LOG_LEVEL", "INFO"))

    if not get_config_or_env("PROMETHEUS_ENABLED"):
        logger.info("Prometheus metrics disabled")
        return

    auth_token = get_config_or_env("PROMETHEUS_AUTH_TOKEN")

    app.wsgi_app = DispatcherMiddleware(
        app.wsgi_app, {"/metrics": make_metrics_wsgi_app(auth_token)}
    )

    REGISTRY.register(MetricsCollector(app, logger))

    logger.info("Prometheus metrics configured")


def make_metrics_wsgi_app(auth_token):
    prometheus_app = make_wsgi_app()

    def metrics_wsgi_app(env, start_response):
        if not auth_token:
            logger.error("No auth token configured!")
            start_response("500 Internal Server Error", [("", "")])
            return [b""]

        auth_header = env.get("HTTP_AUTHORIZATION", "").split(" ")
        if (
            len(auth_header) != 2
            or auth_header[0] != "Bearer"
            or auth_header[1] != auth_token
        ):
            start_response("401 Forbidden", [("", "")])
            return [b""]

        return prometheus_app(env, start_response)

    return metrics_wsgi_app


def get_config_or_env(key):
    return get_app_config(key) or os.getenv(key)
