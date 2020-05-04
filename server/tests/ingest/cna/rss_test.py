
import os
import unittest
import feedparser

from lxml import etree
from datetime import datetime
from ewt.ingest.cna import CNAFeedingService


with open(os.path.join(os.path.dirname(__file__), 'rss.xml')) as f:
    xml = f.read()


class CNA_RSSTestCase(unittest.TestCase):

    def get_item(self, index=0):
        data = feedparser.parse(xml)
        service = CNAFeedingService()
        service.tree = etree.fromstring(xml.encode())
        item = service._create_item(data.entries[index])
        return item

    def test_parse_media(self):
        item = self.get_item()

        self.assertIsNone(item.get('abstract'))
        self.assertIn('<p><em>Archbishop', item['body_html'])

        self.assertEqual(datetime(2020, 4, 16, 11, 0, 0), item['versioncreated'])
        self.assertEqual(item['versioncreated'], item['firstcreated'])

        featured = item['associations']['featuremedia']
        self.assertEqual('tag:www.catholicnewsagency.com:images:pierre_at_2019_mass_for_life.jpeg', featured['guid'])
        self.assertIn('Credit: Christine Rousselle/CNA', featured['description_text'])
        self.assertEqual('Pierre At 2019 Mass For Life', featured['headline'])
        self.assertEqual('Test', featured['creditline'])
        self.assertEqual(item['versioncreated'], featured['versioncreated'])
        self.assertEqual(item['firstcreated'], featured['firstcreated'])
        rend = featured['renditions']['baseImage']
        self.assertIn('mass_for_life.jpeg', rend['href'])

    def test_ignore_shutterstock(self):
        item = self.get_item(1)
        self.assertIsNone(item.get('associations'))

    def test_fix_html(self):
        service = CNAFeedingService()
        self.assertEqual('<a href="--">&#8212;</a>', service._fix_html('<a href="--">--</a>'))
        self.assertEqual("<a href=\"--\">&#8216;foo.&#8217;</a>", service._fix_html("<a href='--'>'foo'.</a>"))
        self.assertEqual('<a href="--">&#8220;foo,&#8221;</a>', service._fix_html('<a href="--">"foo",</a>'))
        self.assertEqual('<p>foo<br>&#8212;</p>', service._fix_html('<p>foo<br>--</p>'))
