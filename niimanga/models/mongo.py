"""
 # Copyright (c) 05 2015 | surya
 # 19/05/15 nanang.ask@kubuskotak.com
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
 #  mongo.py
"""
from datetime import datetime, timedelta

from pymongo import MongoClient
import re
from slugify import slugify


conn = MongoClient('localhost', 27017)
db = conn['niimanga']


def _chapter_slug(str_, slug_manga):
    name = str_
    # print(name[name.index("C"):])
    no = re.search(r"\d+(\.\d+)?", name[name.index("C"):]).group(0)
    # print(no)
    return slugify('{1}-chapter-{0}'.format(no.zfill(3), slug_manga), to_lower=True)


def in_or_up_manga_home(url, manga):
    mangadb = db.manga
    mangadb.update({'manga_url': url}, {'$set': {
        'name': manga.get('name'),
        'rank': manga.get('rank', '0'),
        'tags': manga.get('tags', []),
        'description': manga.get('description', u'')
    }},  upsert=True)
    return mangadb.find_one({'manga_url': url})


def insert_or_update_manga(objs):
    returns = []
    if 'manga' not in db.collection_names():
        db.create_collection('manga')
    mangadb = db.manga

    def _filter_date(slug, newdate):
        if newdate is not None:
            slug = mangadb.find({'slug': slug}).limit(1)
            if slug is not None:
                return datetime.strptime(newdate, '%b %d, %Y %I:%S%p')
        return datetime.now() - timedelta(days=1)

    for manga in objs:
        mangadb.update({'manga_url': manga.get('manga_url')}, {'$set': {
            'status': manga.get('status', u'On going'),
            'genres': manga.get('genres', None),
            'author': manga.get('author', None),
            'manga_url': manga.get('manga_url'),
            'name': manga.get('name'),
            'slug': slugify(manga.get('name'), to_lower=True),
            'last_date': _filter_date(slugify(manga.get('name'), to_lower=True), manga.get('last_date', None)),
            'thumb_url': manga.get('thumb_url'),
            'last_ch_name': manga.get('last_ch_name'),
            'last_ch_chapter': _chapter_slug(manga.get('last_ch_name'), slugify(manga.get('name'), to_lower=True)),
            'rank': int(re.search(r"\d+(\.\d+)?", manga.get('rank', '0')).group(0)),
            'tags': manga.get('tags', []),
            'description': manga.get('description', u''),
            'chapters': manga.get('chapters', [])
        }},  upsert=True)
        manga.update({'slug': slugify(manga.get('name'), to_lower=True)})
        returns.append(db.manga.find_one({'manga_url': manga.get('manga_url')}))
    return returns


def in_or_up_chapters(chapters, slug_manga, manga_url):
    returns = []
    if 'chapter' not in db.collection_names():
        db.create_collection('chapter')
    chapterdb = db.chapter

    for chapter in chapters:
        # print(re.search(r"\d+(\.\d+)?", chapter.get('name', '')).group(0))
        name = chapter.get('name', '')
        # print(name[name.index("C"):])
        no = re.search(r"\d+(\.\d+)?", name[name.index("C"):]).group(0)
        # print(no)
        name = slugify('{1}-chapter-{0}'.format(no.zfill(3), slug_manga), to_lower=True)
        chapterdb.update({'slug': name}, {'$set': {
            'manga_url': manga_url,
            'name': chapter.get('name'),
            'slug': name,
            'url': chapter.get('url'),
            'order': no
        }},  upsert=True)
        # chapter.update({'slug': name})
        returns.append(chapterdb.find_one({'slug': name}))
    return returns


def in_or_up_pages(chapters, slug):
    returns = []
    if 'chapter' not in db.collection_names():
        db.create_collection('chapter')
    chapterdb = db.chapter

    for chapter in chapters:
        chapterdb.update({'slug': slug}, {'$set': {
            'name': chapter.get('name'),
            'prev_url': chapter.get('prev_chapter_url'),
            'next_url': chapter.get('next_chapter_url'),
            'pages': chapter.get('pages', [])
        }},  upsert=True)
        chapter.update({'slug': slugify(chapter.get('name'), to_lower=True)})
        returns.append(chapterdb)
    return returns