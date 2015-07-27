"""
 # Copyright (c) 06 2015 | surya
 # 18/06/15 nanang.ask@kubuskotak.com
 # This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 2
 # of the License, or (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program; if not, write to the Free Software
 # Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 #  test_mmangahere.py
"""
from unittest import TestCase, main

from niimanga.sites import MangaHereMob


site = MangaHereMob()


class SeriesInfo(TestCase):

    def test_normal(self):
        url = 'http://m.mangahere.co/manga/shokugeki_no_soma/'
        info = site.series_info(site.fetch_manga_seed_page(url))
        self.assertIsInstance(info, dict)

        # Attributes that can be asserted by exact value:
        expected = {
            'name': 'Shokugeki no Soma',
            'site': 'm.mangahere.co',
            'thumb_url': 'http://a.mhcdn.net/store/manga/12114/thumb_cover.jpg?v=1434335239',
            'tags': [{'url': 'comedy', 'tag': 'Comedy'},
                     {'url': 'drama', 'tag': 'Drama'},
                     {'url': 'ecchi', 'tag': 'Ecchi'},
                     {'url': 'romance', 'tag': 'Romance'},
                     {'url': 'school_life', 'tag': 'School Life'},
                     {'url': 'shounen', 'tag': 'Shounen'},
                     {'url': 'slice_of_life', 'tag': 'Slice of Life'}
                     ],
            'authors': ['TSUKUDA Yuuto'],
            'status': 'status: ongoing',
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


if __name__ == '__main__':
    main()