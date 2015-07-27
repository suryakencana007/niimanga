"""
 # Copyright (c) 03 2015 | surya
 # 16/03/15 nanang.ask@kubuskotak.com
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
 #  schema.py
"""
from niimanga.libs.utils import guid
from slugify import slugify
from sqlalchemy import event, Column, ForeignKeyConstraint, DateTime, Table, CHAR, Unicode, Integer, SMALLINT, FLOAT
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym
from sqlalchemy.sql import functions


class Followers(object):
    viewed = Column(Integer, default=0)
    rating = Column(FLOAT, default=0.0)
    votes = Column(Integer, default=0)
    # generate untuk posisi rank
    rank = Column(Integer, default=0)


class Slugger(object):

    _slug = Column('slug', Unicode(200), unique=True)

    def _set_slug(self, name):
        self._slug = slugify(name, to_lower=True)

    def _get_slug(self):
        return self._slug

    """it's cool alias routed"""
    @declared_attr
    def slug(cls):
        return synonym('_slug', descriptor=property(cls._get_slug,
                                                    cls._set_slug))


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class."""

    # id = Column(Integer, primary_key=True)
    id = Column(CHAR(10), primary_key=True, default=guid)


class References(object):
    """A mixin which creates foreign key references to related classes."""
    _to_ref = set()
    _references = _to_ref.add

    @classmethod
    def __declare_first__(cls):
        """declarative hook called within the 'before_configure' mapper event."""
        for lcl, rmt in cls._to_ref:
            cls._decl_class_registry[lcl]._reference_table(
                cls._decl_class_registry[rmt].__table__)
        cls._to_ref.clear()

    @classmethod
    def _reference_table(cls, ref_table):
        """Create a foreign key reference from the local class to the given remote
        table.

        Adds column references to the declarative class and adds a
        ForeignKeyConstraint.

        """
        # create pairs of (Foreign key column, primary key column)
        cols = [(Column(), refcol) for refcol in ref_table.primary_key]

        # set "tablename_colname = Foreign key Column" on the local class
        for col, refcol in cols:
            setattr(cls, "%s_%s" % (ref_table.name, refcol.name), col)

        # add a ForeignKeyConstraint([local columns], [remote columns])
        cls.__table__.append_constraint(ForeignKeyConstraint(*zip(*cols)))


class utcnow(functions.FunctionElement):
    key = 'utcnow'
    type = DateTime(timezone=True)


@compiles(utcnow)
def _default_utcnow(element, compiler, **kw):
    """default compilation handler.

    Note that there is no SQL "utcnow()" function; this is a
    "fake" string so that we can produce SQL strings that are dialect-agnostic,
    such as within tests.

    """
    return "utcnow()"


@compiles(utcnow, 'postgresql')
def _pg_utcnow(element, compiler, **kw):
    """Postgresql-specific compilation handler."""

    return "(CURRENT_TIMESTAMP AT TIME ZONE 'utc')::TIMESTAMP WITH TIME ZONE"


@event.listens_for(Table, "after_parent_attach")
def timestamp_cols(table, metadata):
    from .base import Base

    if metadata is Base.metadata:
        table.append_column(
            Column('created_at',
                   DateTime(timezone=True),
                   nullable=False, default=utcnow())
        )
        table.append_column(
            Column('updated_at',
                   DateTime(timezone=True),
                   nullable=False,
                   default=utcnow(), onupdate=utcnow())
        )

