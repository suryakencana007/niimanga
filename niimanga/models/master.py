"""
 # Copyright (c) 04 2015 | surya
 # 29/04/15 nanang.ask@kubuskotak.com
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
 #  master.py
"""
from niimanga.models import Base
from niimanga.models.meta.schema import Slugger, SurrogatePK
from sqlalchemy import Column, Unicode, Text, CHAR

# category
DORAMA = ("JD", "dorama")
ANIME = ("AN", "anime")
KDRAMA = ("KD", "kdrama")


class GenreMgr(object):
    @staticmethod
    def from_string(genre_str):
        if not genre_str or '' not in genre_str:
            return {}

        genre_list = set([genre.lower().strip() for genre in genre_str.split(",")])
        genre_dict = {}

        for genre in GenreMgr.find(genres=genre_list):
            genre_dict[genre.name.lower()] = genre
            genre_list.remove(genre.name.lower())

        for new_genre in (genre for genre in genre_list if genre != ''):
            genre_dict[new_genre] = Genre(new_genre)

        return genre_dict

    @staticmethod
    def find(order_by=None, genres=None):
        qry = Genre.query

        if genres:
            qry = qry.filter(Genre.name.in_(genres))

        if order_by:
            qry = qry.order_by(order_by)
        else:
            qry = qry.order_by(Genre.name)

        return qry.all()


class Genre(Slugger, SurrogatePK, Base):
    __tablename__ = u'tb_genre'

    name = Column('genre_name', Unicode(100))
    # slug = Column(Unicode(200), unique=True)
    description = Column('genre_desc', Text, default=u'')

    def __init__(self, name, desc=None):
        self.name = name.lower()
        self.slug = name
        self.description = desc


class AuthorMgr(object):
    @staticmethod
    def from_string(author_str):
        if not author_str or '' not in author_str:
            return {}

        author_list = set([author.lower().strip() for author in author_str.split(",")])
        author_dict = {}

        for author in AuthorMgr.find(authors=author_list):
            author_dict[author.name.lower()] = author
            author_list.remove(author.name.lower())

        for new_author in (author for author in author_list if author != ""):
            author_dict[new_author] = Author(new_author)

        return author_dict

    @staticmethod
    def find(order_by=None, authors=None):
        qry = Author.query

        if authors:
            qry = qry.filter(Author.name.in_(authors))

        if order_by:
            qry = qry.order_by(order_by)
        else:
            qry = qry.order_by(Author.name)

        return qry.all()


class Author(Slugger, SurrogatePK, Base):
    __tablename__ = u'tb_author'

    name = Column('author_name', Unicode(100))
    # slug = Column(Unicode(200), unique=True)

    def __init__(self, name):
        self.name = name.lower()
        self.slug = name


class ArtistMgr(object):
    @staticmethod
    def from_string(artist_str):
        if not artist_str or '' not in artist_str:
            return {}

        artist_list = set([artist.lower().strip() for artist in artist_str.split(",")])
        artist_dict = {}

        for artist in ArtistMgr.find(artist=artist_list):
            artist_dict[artist.name.lower()] = artist
            artist_list.remove(artist.name.lower())

        for new_artist in (artist for artist in artist_list if artist != ""):
            artist_dict[new_artist] = Artist(new_artist)

        return artist_dict

    @staticmethod
    def find(order_by=None, artist=None):
        qry = Artist.query

        if artist:
            qry = qry.filter(Artist.name.in_(artist))

        if order_by:
            qry = qry.order_by(order_by)
        else:
            qry = qry.order_by(Artist.name)

        return qry.all()

ACT = ('AC', "act")
VOICE = ('VC', "voice")
DRAW = ('DW', "drawer")


class Artist(Slugger, SurrogatePK, Base):
    __tablename__ = u'tb_artist'

    name = Column('artist_name', Unicode(100))
    ability = Column('artist_ability', CHAR(2))

    # characters = one_to_many("Character",
    #                          backref="artist",
    #                          lazy="joined", innerjoin=True)

    def __init__(self, name, ability=DRAW[0], lang="JP"):
        self.name = name.lower()
        self.slug = name
        self.ability = ability
        self.language = lang


class CharMgr(object):
    @staticmethod
    def from_string(char_str):
        if not char_str or '' not in char_str:
            return {}

        char_list = set([char.lower().strip() for char in char_str.split(",")])
        char_dict = {}

        for char in CharMgr.find(char=char_list):
            char_dict[char.name.lower()] = char
            char_list.remove(char.name.lower())

        for new_char in (char for char in char_list if char != ''):
            char_dict[new_char] = Character(new_char)

        return char_dict

    @staticmethod
    def find(order_by=None, chars=None):
        qry = Character.query

        if chars:
            qry = qry.filter(Character.name.in_(chars))

        if order_by:
            qry = qry.order_by(order_by)
        else:
            qry = qry.order_by(Character.name)

        return qry.all()


class Character(Slugger, SurrogatePK, Base):
    __tablename__ = u'tb_character'

    name = Column('character_name', Unicode(100))
    rules = Column('character_rules', Unicode(100))

    def __init__(self, name, rules):
        self.name = name
        self.slug = name
        self.rules = rules


class Staff(Slugger, SurrogatePK, Base):
    __tablename__ = u'tb_staff'

    name = Column('staff_name', Unicode(100))

    def __init__(self, name):
        self.name = name
        self.slug = name


class Season(Slugger, SurrogatePK, Base):
    __tablename__ = u'tb_season'

    title = Column(Unicode(255))
    # DORAMA = ("JD", "dorama"), ANIME = ("AN", "anime"), KDRAMA = ("KD", "kdrama")
    category = Column(CHAR(2), default="JD")
    # ["Winter", "Spring"]
    type = Column(CHAR(6), default="winter")
    year = Column(CHAR(4))

    def __init__(self, title, category=None, type=None, year=0):
        self.title = title
        self.slug = title
        self.category = category
        self.type = type
        self.year = year


class ISOLang(SurrogatePK, Base):
    __tablename__ = u'tb_lang'

    name = Column(Unicode(50))
    iso = Column(CHAR(2))

    def __init__(self, name, iso):
        self.name = name
        self.iso = iso