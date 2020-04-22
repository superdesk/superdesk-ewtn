
from superdesk.io.registry import register_feeding_service, register_feeding_service_parser

from .rss import CNAFeedingService


def init_app(_app):
    register_feeding_service(CNAFeedingService)
    register_feeding_service_parser(CNAFeedingService.NAME, None)
