import arrow
import click
import superdesk

from superdesk.commands import cli


@cli.command("fix_timestamps")
@click.option("--limit", "-l", type=int, default=0)
async def fix_timestamps(limit=0):
    """Set versioncreated from extra.original_published_at for archive and published items."""
    lookup = {"extra.original_published_at": {"$ne": None}}
    archive_service = superdesk.get_resource_service("archive")
    published_service = superdesk.get_resource_service("published")
    items = await archive_service.get_from_mongo_async(req=None, lookup=lookup)
    updated = 0
    async for item in items:
        try:
            published = arrow.get(item["extra"]["original_published_at"]).datetime
        except ValueError:
            continue
        updates = {"versioncreated": published}
        print("updating item {} published at {}".format(item["_id"], published))
        await archive_service.system_update_async(item["_id"], updates, item)
        await published_service.update_published_items(
            item["_id"], "versioncreated", updates["versioncreated"]
        )
        updated += 1
        if limit and updated >= limit:
            break
    print("done updating {} items".format(updated))
