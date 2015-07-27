"""
 # Copyright (c) 04 2015 | surya
 # 17/04/15 nanang.ask@kubuskotak.com
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
 #  manga.py
"""
import logging
from datetime import datetime

from niimanga.models import Base
from niimanga.models.master import Genre, Author, GenreMgr, AuthorMgr, Artist, ArtistMgr, ISOLang
from niimanga.models.meta.orm import many_to_one
from niimanga.models.meta.schema import SurrogatePK, Slugger
from sqlalchemy import Column, Unicode, Text, Integer, SMALLINT, FLOAT, CHAR, ForeignKey, DateTime, TIMESTAMP, Float, \
    INTEGER, desc
from sqlalchemy.orm import relation, aliased, contains_eager
from sqlalchemy.orm.collections import attribute_mapped_collection

LOG = logging.getLogger(__name__)

NEW = 0
ONGOING = 1
COMPLETED = 2


class Manga(Slugger, SurrogatePK, Base):

    __tablename__ = u'tb_manga'

    thumb = Column('thumb', Unicode(255))
    title = Column('manga_title', Unicode(255))
    aka = Column('manga_title_aka', Text)
    description = Column('manga_desc', Text)
    status = Column(SMALLINT)

    # ja, ko, zh, ar, ot
    category = Column(CHAR(2))
    # sp, kk, bt(batoto), ed(mangaeden)
    type = Column(CHAR(2))

    # khususon scrap
    origin = Column(Unicode(255))

    viewed = Column(Integer, default=0)
    rating = Column(FLOAT, default=0.0)
    votes = Column(Integer, default=0)

    # generate untuk posisi rank
    rank = Column(Integer, default=9999)

    chapter_count = Column(Integer, default=0)
    chapter_updated = Column(DateTime, default=datetime.utcnow())

    released = Column(Integer, default=0)

    genres = relation(
        Genre,
        backref="manga",
        collection_class=attribute_mapped_collection('name'),
        secondary='genre_manga',
        lazy='joined',
        innerjoin=False
    )

    authors = relation(
        Author,
        backref="manga",
        collection_class=attribute_mapped_collection('name'),
        secondary='author_manga',
        lazy='joined',
        innerjoin=False
    )

    artist = relation(
        Artist,
        backref="manga",
        collection_class=attribute_mapped_collection('name'),
        secondary='artist_manga',
        lazy='joined',
        innerjoin=False
    )

    def __init__(self, tipe, title, released, genres=None, authors=None, artist=None, alt=None, desc=None, status=ONGOING):
        self.type = tipe
        self.title = title
        self.released = released
        self.slug = "-".join([tipe, title])
        self.aka = alt
        self.description = desc
        self.status = status

        self.genres = GenreMgr.from_string(genres) if genres else {}

        self.authors = AuthorMgr.from_string(authors) if authors else {}

        self.artist = ArtistMgr.from_string(artist) if artist else {}

    def mark_on_going(self):
        self.status = ONGOING

    def mark_completed(self):
        self.status = COMPLETED

    def updated_chapter(self):
        self.chapter_count += 1
        self.chapter_updated = datetime.utcnow()

    def updated_viewed(self):
        self.viewed += 1

    def get_genre_tostr(self):
        return ", ".join(str(genre.encode("utf-8")).capitalize() for genre in self.genres.iterkeys())

    def set_genres(self, genre_str):
        self.genres = GenreMgr.from_string(genre_str)

    def get_authors(self):
        return ", ".join(str(author.encode("utf-8")).capitalize() for author in self.authors.iterkeys())

    def set_authors(self, author_str):
        self.authors = AuthorMgr.from_string(author_str)

    def get_artist(self):
        return ", ".join(str(artist.encode("utf-8")).capitalize() for artist in self.artist.iterkeys())

    def set_artist(self, artist_str):
        self.artist = ArtistMgr.from_string(artist_str)

        # # clear the list first
        # while self.tags:
        #     del self.tags[0]
        # # add new tags
        # for tag in value:
        #     self.tags.append(self._find_or_create_tag(tag))

    # genre_to_string = property(_get_genre_tostr,
    #                            _set_genres,
    #                            u'Property untuk many to many genre relation')

    @classmethod
    def last_chapter(cls, manga_id):
        return Chapter.query \
            .filter_by(tb_manga_id=manga_id) \
            .order_by(desc(Chapter.updated)) \
            .first()

    @classmethod
    def last_ch_no(cls, manga_id):
        return cls._gen_chapter(cls.lastd_chapter(manga_id).number)

    @classmethod
    def _gen_chapter(cls, ch):
        return "{0:03d}".format(ch)

    @classmethod
    def get_chapter(cls, manga, ch):
        # slug = "{0}-{1}".format(manga.slug, ch)
        LOG.debug(ch)
        return Chapter.query \
            .filter_by(tb_manga_id=manga.id) \
            .filter(Chapter.slug == ch) \
            .first()

    @classmethod
    def popular(cls, limit=50, page=0, with_genres=False):
        """Get the Mangas by most popular"""

        qry = Manga.query

        offset = limit * page
        qry = qry.order_by(Manga.viewed.desc()) \
            .limit(limit) \
            .offset(offset) \
            .from_self()

        genres = aliased(Genre)
        if with_genres:
            qry = qry.outerjoin(genres, Manga.genres) \
                .options(contains_eager(Manga.genres,
                                        alias=genres))
        return qry.all()

    @classmethod
    def recent(cls, limit=50, page=0, with_genres=False):
        """Get a recent set of Manga Chapter Updated"""

        qry = Manga.query

        offset = limit * page
        qry = qry. \
            filter(Manga.chapter_count > 0). \
            order_by(Manga.chapter_updated.desc()) \
            .limit(limit) \
            .offset(offset) \
            .from_self()

        if with_genres:
            qry = qry.outerjoin(Manga.genres) \
                .options(contains_eager(Manga.genres))

        return qry.all()


class GenreManga(Base):

    __tablename__ = u'genre_manga'

    manga_id = Column(CHAR(10), ForeignKey('tb_manga.id'), primary_key=True)
    genre_id = Column(CHAR(10), ForeignKey('tb_genre.id'), primary_key=True)


class AuthorManga(Base):

    __tablename__ = u'author_manga'

    manga_id = Column(CHAR(10), ForeignKey('tb_manga.id'), primary_key=True)
    author_id = Column(CHAR(10), ForeignKey('tb_author.id'), primary_key=True)


class ArtistManga(Base):

    __tablename__ = u'artist_manga'

    manga_id = Column(CHAR(10), ForeignKey('tb_manga.id'), primary_key=True)
    artis_id = Column(CHAR(10), ForeignKey('tb_artist.id'), primary_key=True)


class Chapter(Slugger, SurrogatePK, Base):

    __tablename__ = u'tb_chapter'

    title = Column('chapter_title', Unicode(200))

    prefix = Column('chapter_prefix_image', CHAR(1), default='i')

    chapter = Column('chapter_no', Float(precision=1), default=0)
    volume = Column('chapter_vol', SMALLINT)

    updated = Column('chapter_updated', TIMESTAMP)
    viewed = Column(INTEGER, default=0)

    lang_id = Column(CHAR(10), ForeignKey(ISOLang.id))
    lang = relation(ISOLang, uselist=False)
    # sort order berguna untuk urutan chapter e.g data chapter nisekoi lang "en" asc sortorder
    sortorder = Column('chapter_sort', INTEGER)

    manga = many_to_one("Manga",
                        backref="chapter",
                        lazy="joined", innerjoin=True)

    def __init__(self, title, chapter, volume, prefix=u'i'):
        self.title = title
        self.chapter = chapter
        self.volume = volume
        self.prefix = prefix

    def updated_viewed(self):
        self.viewed += 1