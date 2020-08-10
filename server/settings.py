#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
from pathlib import Path


def env(variable, fallback_value=None):
    env_value = os.environ.get(variable, '')
    if len(env_value) == 0:
        return fallback_value
    else:
        if env_value == "__EMPTY__":
            return ''
        else:
            return env_value


ABS_PATH = str(Path(__file__).resolve().parent)

init_data = Path(ABS_PATH) / 'data'
if init_data.exists():
    INIT_DATA_PATH = init_data

RENDITIONS = {
    'picture': {
        'thumbnail': {'width': 220, 'height': 120},
        'viewImage': {'width': 640, 'height': 640},
        'baseImage': {'width': 1400, 'height': 1400},
    },
    'avatar': {
        'thumbnail': {'width': 60, 'height': 60},
        'viewImage': {'width': 200, 'height': 200},
    }
}

WS_HOST = env('WSHOST', '0.0.0.0')
WS_PORT = env('WSPORT', '5100')

LOG_CONFIG_FILE = env('LOG_CONFIG_FILE', 'logging_config.yml')

REDIS_URL = env('REDIS_URL', 'redis://localhost:6379')
if env('REDIS_PORT'):
    REDIS_URL = env('REDIS_PORT').replace('tcp:', 'redis:')
BROKER_URL = env('CELERY_BROKER_URL', REDIS_URL)

SECRET_KEY = env('SECRET_KEY', '')

# publishing associations with the main item (images etc.)
PUBLISH_ASSOCIATED_ITEMS = True

# storing published keywords in a CV
KEYWORDS_ADD_MISSING_ON_PUBLISH = True

# media required fields
VALIDATOR_MEDIA_METADATA = {
    "headline": {
        "required": False,
    },
    "alt_text": {
        "required": False,
    },
    "archive_description": {
        "required": False,
    },
    "description_text": {
        "required": False,
        "textarea": True,
    },
    "copyrightholder": {
        "required": False,
    },
    "byline": {
        "required": False,
    },
    "usageterms": {
        "required": False,
    },
    "copyrightnotice": {
        "required": False,
    },
}

# schema for images, video, audio
SCHEMA = {
    'picture': {
        'headline': {'required': False},
        'description_text': {'required': False, 'textarea': True},
        'alt_text': {'required': False},
        'byline': {'required': False},
        'sign_off': {'required': False}
    },
    'video': {
        'headline': {'required': False},
        'description_text': {'required': True},
        'byline': {'required': False},
        'sign_off': {'required': False}
    },
    'graphic': {
        'headline': {'required': False},
        'description_text': {'required': True},
        'byline': {'required': False},
        'sign_off': {'required': False}
    },
}


# editor for images, video, audio
EDITOR = {
    'picture': {
        'headline': {'order': 1, 'sdWidth': 'full'},
        'description_text': {'order': 2, 'sdWidth': 'full', 'textarea': True},
        'byline': {'order': 3, 'sdWidth': 'full'},
        'sign_off': {'displayOnMediaEditor': False},
        'archive_description': {'displayOnMediaEditor': False}
    },
    'video': {
        'slugline': {'order': 1, 'sdWidth': 'full'},
        'headline': {'order': 2, 'sdWidth': 'full'},
        'description_text': {'order': 3, 'sdWidth': 'full', 'textarea': True},
        'media_type': {'order': 4, 'sdWidth': 'full'},
        'byline': {'order': 5, 'sdWidth': 'full'},
        'sign_off': {'displayOnMediaEditor': False},
        'archive_description': {'displayOnMediaEditor': False}
    },
    'graphic': {
        'headline': {'order': 1, 'sdWidth': 'full'},
        'description_text': {'order': 2, 'sdWidth': 'full', 'textarea': True},
        'byline': {'order': 3, 'sdWidth': 'full'},
        'sign_off': {'displayOnMediaEditor': False},
        'archive_description': {'displayOnMediaEditor': False}
    },
}

SCHEMA['audio'] = SCHEMA['video']
EDITOR['audio'] = EDITOR['video']

INSTALLED_APPS = (
    'ewt.ingest.cna',
)

GEONAMES_USERNAME = env('GEONAMESUSERNAME')
GEONAMES_FEATURE_CLASSES = ['A', 'P']
