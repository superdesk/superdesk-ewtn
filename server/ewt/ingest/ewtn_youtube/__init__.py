
from superdesk.io.registry import register_feeding_service, register_feeding_service_parser

from .rss import EWTNYoutubeFeedingService


def init_app(_app):
    register_feeding_service(EWTNYoutubeFeedingService)
    register_feeding_service_parser(EWTNYoutubeFeedingService.NAME, None)
