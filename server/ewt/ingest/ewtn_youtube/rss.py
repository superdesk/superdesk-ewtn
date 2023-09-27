
import re
import lxml.html
import lxml.etree

from superdesk.io.feeding_services.rss import RSSFeedingService, generate_tag_from_url


NSMAP = {
    'media': 'http://search.yahoo.com/mrss/',
    None: 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015'
}


class EWTNYoutubeFeedingService(RSSFeedingService):
    NAME = 'ewtn youtube rss'
    label = 'EWTN Youtube RSS'

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
            xml_item for xml_item in self.tree.findall('entry', NSMAP)
            if xml_item.find('yt:videoId', NSMAP).text == data.yt_videoid
        ), None)

    def _create_item(self, data, field_aliases=None, source='source'):
        item = super()._create_item(data, field_aliases, source)
        item['headline'] = self._fix_text(item['headline'])
        item['abstract'] = self._substring_before("----", item["abstract"]).strip()
        item['abstract'] = self._substring_before("————", item["abstract"]).strip()
        item['abstract'] = self._substring_before("Subscribe to EWTN’s YouTube Channel", item["abstract"]).strip()
        if len(item['abstract']) == 0:
            item['abstract'] = item['headline']
        item['abstract'] = self._fix_text(item['abstract'])
        item['body_html'] = self._fix_html(item["abstract"])
        item['subject'] = [
            {
                "name": "Video",
                "qcode": "video",
                "scheme": "atype"
            }
        ]
        xml_item = self._get_xml_item(data)
        yt_video_link = xml_item.find("media:group", NSMAP).find("media:content", NSMAP).attrib["url"]
        item['body_html'] = item['body_html'] + f"<p>Video link: {yt_video_link}</p>"
        media_title = xml_item.find('media:group', NSMAP).find('media:title', NSMAP).text.strip()
        thumbnail = xml_item.find("media:group", NSMAP).find("media:thumbnail", NSMAP)
        rendition = {
            'href': thumbnail.attrib['url'],
            'width': int(thumbnail.attrib['width']),
            'height': int(thumbnail.attrib['height']),
            'mimetype': "image/jpeg",
        }
        item['associations'] = {
            'featuremedia': {
                'type': 'picture',
                'guid': generate_tag_from_url(thumbnail.attrib['url']),
                'headline': media_title,
                'byline': '',
                'creditline': '',
                'description_text': '',
                'firstcreated': item['versioncreated'],
                'versioncreated': item['versioncreated'],
                'renditions': {
                    'original': rendition.copy(),
                    'baseImage': rendition.copy(),
                    'viewImage': rendition.copy(),
                },
            },
        }
        return item

    def _substring_before(self, needle, haystack):
        return haystack.split(needle)[0]

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
