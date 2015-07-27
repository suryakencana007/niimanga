import json
import logging
from unittest import TestCase, main

from niimanga.sites.batoto import Batoto
from niimanga.tasks.batoto import build_from_latest


site = Batoto()

LOG = logging.getLogger(__name__)


class SeriesInfo(TestCase):

    def test_normal(self):
        # url = 'http://bato.to/comic/_/comics/shokugeki-no-soma-r7530'
        url = 'http://localhost:8234/High-School%20DxD%20-%20Scanlations%20-%20Comic%20-%20Comic%20Directory%20-%20Batoto%20-%20Batoto.html'
        info = site.series_info(site.fetch_manga_seed_page(url))
        print(json.dumps(info, sort_keys=True, indent=4, separators=(',', ': ')))
        self.assertIsInstance(info, dict)

        # Attributes that can be asserted by exact value:
        expected = {
            'name': 'Shokugeki No Soma',
            'site': 'batoto',
            'thumb_url': 'http://img.bato.to/forums/uploads/effd6e0d6d42602b4c29bb5c1c1ba5e4.jpg',
            'tags': ['comedy', 'doujinshi', 'supernatural', 'tragedy'],
            'authors': ['Makegumi Club (Circle)', 'Matsuri', 'Wasu', 'Zephyr'],
            'status': 'complete',
            }
        for key, val in expected.iteritems():
            print '>>> Asserting', key
            print '>>>>>>', info[key]
            print '======================='
            self.assertEqual(info[key], val)

        # The rest:

        self.assertIsInstance(info['description'], list)
        for d in info['description']:
            self.assertIsInstance(d, unicode)

        self.assertIsInstance(info['status'], unicode)

        chapters = info['chapters']
        self.assertIsInstance(chapters, list)
        self.assertTrue(len(chapters) == 2)
        for chap in chapters:
            self.assertIsInstance(chap, dict)
            self.assertIn('url', chap)
            self.assertIn('name', chap)


class SearchByAuthor(TestCase):

    def test_normal(self):

        series_list = site.search_by_author('Fujiko F. Fujio')
        print '>>> Got list:'
        for s in series_list:
            print s
        self.assertEquals(series_list, [
            {
                'name': 'Daichouhen Doraemon',
                'url': 'http://bato.to/comic/_/daichouhen-doraemon-r5414',
                'site': 'batoto',
                },
            {
                'name': 'Doraemon',
                'url': 'http://bato.to/comic/_/doraemon-r1791',
                'site': 'batoto',
                },
            {
                'name': 'Doraemon - Doranote (Doujinshi)',
                'url': 'http://bato.to/comic/_/doraemon-doranote-doujinshi-r7663',
                'site': 'batoto',
                },
            {
                'name': 'The Doraemons - Doraemon Game Comic',
                'url': 'http://bato.to/comic/_/the-doraemons-doraemon-game-comic-r11386',
                'site': 'batoto',
                },
            ])


class SearchLatest(TestCase):

    def test_normal(self):
        print(site.search_latest())


class LatestToDB(TestCase):

    def test_normal(self):

        for i, source in enumerate(site.search_latest()):
            # LOG.info(source)
            print(source)
            build_from_latest(site, source)

if __name__ == '__main__':
    main()