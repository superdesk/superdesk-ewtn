
import os
import unittest
import feedparser

from lxml import etree
from datetime import datetime
from ewt.ingest.ewtn_youtube import EWTNYoutubeFeedingService


with open(os.path.join(os.path.dirname(__file__), 'rss.xml'), encoding="utf-8") as f:
    xml = f.read()


NSMAP = {
    'media': 'http://search.yahoo.com/mrss/',
    None: 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015'
}


class EWNTYoutube_RSSTestCase(unittest.TestCase):

    def get_item(self, index=0):
        data = feedparser.parse(xml)
        service = EWTNYoutubeFeedingService()
        service.tree = etree.fromstring(xml.encode())
        item = service._create_item(data.entries[index])
        return item

    def test_parse_entry(self):
        item = self.get_item()

        self.assertIn("From the Basilica of the National Shrine of the Immaculate Conception", item['abstract'])
        self.assertNotIn("Subscribe to EWTN’s YouTube Channel", item['abstract'])
        self.assertIn("From the Basilica of the National Shrine of the Immaculate Conception", item['body_html'])
        self.assertNotIn("Subscribe to EWTN’s YouTube Channel", item['body_html'])
        self.assertEqual('EWTN', item['byline'])

        self.assertEqual(datetime(2023, 9, 1, 12, 8, 55), item['firstcreated'])
        self.assertEqual(datetime(2023, 9, 1, 12, 37, 46), item['versioncreated'])

        featured = item['associations']['featuremedia']
        self.assertEqual('tag:i3.ytimg.com:vi:2JELmDmKJlA:hqdefault.jpg', featured['guid'])
        # self.assertIn('Credit: Christine Rousselle/CNA', featured['description_text'])
        self.assertEqual('THE CATHOLIC UNIVERSITY OF AMERICA: MASS OF THE HOLY SPIRIT - 2023-08-31',
                         featured['headline'])
        self.assertEqual('', featured['creditline'])
        self.assertEqual('', featured['byline'])
        self.assertEqual(item['versioncreated'], featured['versioncreated'])
        self.assertEqual(item['versioncreated'], featured['firstcreated'])
        rend = featured['renditions']['baseImage']
        self.assertEqual('https://i3.ytimg.com/vi/2JELmDmKJlA/hqdefault.jpg', rend['href'])

    def test_fix_html(self):
        service = EWTNYoutubeFeedingService()
        self.assertEqual('<a href="--">&#8212;</a>', service._fix_html('<a href="--">--</a>'))
        self.assertEqual("<a href=\"--\">&#8216;foo.&#8217;</a>", service._fix_html("<a href='--'>'foo'.</a>"))
        self.assertEqual('<a href="--">&#8220;foo,&#8221;</a>', service._fix_html('<a href="--">"foo",</a>'))
        self.assertEqual('<p>foo<br>&#8212;</p>', service._fix_html('<p>foo<br>--</p>'))
