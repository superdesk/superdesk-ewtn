
import re
import lxml.html
import lxml.etree

from superdesk.io.feeding_services.rss import RSSFeedingService, generate_tag_from_url


NSMAP = {
    'media': 'http://search.yahoo.com/mrss/',
}

MEDIA_BLACKLIST = (
    'Getty',
    'Shutterstock',
)


class CNAFeedingService(RSSFeedingService):
    NAME = 'cna rss'
    label = 'CNA RSS'

    def _extract_image_links(self, rss_entry):
        """NOOP, image will be associated via _create_item"""
        return []

    def _fetch_data(self):
        """Store XML for later parsing."""
        xml = super()._fetch_data()
        self.tree = lxml.etree.fromstring(xml)
        return xml

    def _get_xml_item(self, data):
        return next((
            xml_item for xml_item in self.tree.find('channel').findall('item')
            if xml_item.find('guid').text == data.guid
        ), None)

    def _create_item(self, data, field_aliases=None, source='source'):
        item = super()._create_item(data, field_aliases, source)
        item['body_html'] = self._fix_html(data.summary_detail['value'])
        item.pop('abstract', None)
        media = getattr(data, 'media_content', None)
        content = getattr(data, 'content', None)
        xml_item = self._get_xml_item(data)
        if media and content:
            for featured in media:
                try:
                    media_credit = xml_item.find('media:content', NSMAP).find('media:credit', NSMAP).text
                except AttributeError:
                    media_credit = None
                if media_credit and any([provider in media_credit for provider in MEDIA_BLACKLIST]):
                    continue
                try:
                    media_title = xml_item.find('media:content', NSMAP).find('media:title', NSMAP).text
                except AttributeError:
                    media_title = ''
                rendition = {
                    'href': featured['url'],
                    'width': int(featured['width']),
                    'height': int(featured['height']),
                    'mimetype': featured['type'],
                }
                item['associations'] = {
                    'featuremedia': {
                        'type': 'picture',
                        'guid': generate_tag_from_url(featured['url']),
                        'headline': media_title,
                        'byline': media_credit or '',
                        'creditline': media_credit or '',
                        'description_text': content[0]['value'],
                        'firstcreated': item['versioncreated'],
                        'versioncreated': item['versioncreated'],
                        'renditions': {
                            'baseImage': rendition.copy(),
                            'viewImage': rendition.copy(),
                        },
                    },
                }
                break  # just need one featured image
        return item

    def _fix_text(self, text):
        text = text \
            .replace('--', '\u2014') \
            .replace('<p><br />', '<p>')
        text = re.sub(r'([\'"])([,.])', r'\2\1', text)  # put ., before closing quote
        text = re.sub(r"'(.+?)'", '\u2018\\1\u2019', text)  # single quotes to smart
        text = re.sub(r'"(.+?)"', '\u201C\\1\u201D', text)  # double quotes to smart
        return text

    def _fix_html(self, value):
        html = lxml.html.fromstring(value)

        for elem in html.iter():
            if elem.text:
                elem.text = self._fix_text(elem.text)
            if elem.tail:
                elem.tail = self._fix_text(elem.tail)

        return lxml.html.tostring(html).decode()
