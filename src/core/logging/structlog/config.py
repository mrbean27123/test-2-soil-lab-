import logging
import sys
from typing import Any

import structlog

import core.context as context


def add_context_data(_, __, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Structlog processor to add context data from contextvars."""
    event_dict["correlation_id"] = context.get_correlation_id()

    event_dict["request_path"] = context.get_request_path()
    event_dict["request_method"] = context.get_request_method()

    current_user = context.get_current_user()
    event_dict["user_id"] = current_user.id if current_user else None

    return event_dict


def configure_logging(log_level: str, environment: str) -> None:
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        add_context_data
    ]

    renderer_processor = (
        structlog.processors.JSONRenderer()
        if environment == "production"
        else structlog.dev.ConsoleRenderer()
    )

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer_processor
        ],
        wrapper_class=structlog.stdlib.BoundLogger or None,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(log_level.upper())
