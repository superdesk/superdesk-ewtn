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

"""Superdesk Manager"""

import arrow
import superdesk

from flask_script import Manager
from app import get_app

app = get_app()
manager = Manager(app)


@manager.option('-l', '--limit', type=int)
def fix_timestamps(limit=0):
    lookup = {'extra.original_published_at': {'$ne': None}}
    items = superdesk.get_resource_service('archive').get_from_mongo(req=None, lookup=lookup)
    updated = 0
    for item in items:
        try:
            published = arrow.get(item['extra']['original_published_at']).datetime
        except ValueError:
            continue
        updates = {'versioncreated': published}
        print('updating item {} published at {}'.format(item['_id'], published))
        superdesk.get_resource_service('archive').system_update(item['_id'], updates, item)
        superdesk.get_resource_service('published').update_published_items(item['_id'], 'versioncreated',
                                                                           updates['versioncreated'])
        updated += 1
        if limit and updated >= limit:
            break
    print('done updating {} items'.format(updated))


if __name__ == '__main__':
    manager.run(superdesk.COMMANDS)
