"""
 # Copyright (c) 05 2015 | surya
 # 05/05/15 nanang.ask@kubuskotak.com
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
 #  component.py
"""
import logging

from niimanga.models import Base
from niimanga.models.master import ANIME
from niimanga.models.meta.orm import many_to_one
from niimanga.models.meta.schema import SurrogatePK, Slugger
from sqlalchemy import Column, Unicode, CHAR, ForeignKey
from sqlalchemy.orm import relation


LOG = logging.getLogger(__name__)


class Slider(Slugger, SurrogatePK, Base):

    __tablename__ = u'comp_slider'

    name = Column(Unicode(100))
    # [HR = header, BT = Bottom, MD = Middle]
    type = Column('comp_type', CHAR(2), default="HR")
    # DORAMA = ("JD", "dorama"), ANIME = ("AN", "anime"), KDRAMA = ("KD", "kdrama")
    category = Column(CHAR(2), default=ANIME[0])

    def __init__(self, name, category, type="HD"):
        self.name = name
        self.slug = name
        self.category = category
        self.type = type


class SliderImage(SurrogatePK, Base):

    __tablename__ = u'slider_image'

    image = Column('image_url', Unicode(200))
    url = Column('link_url', Unicode(200))

    sliders = many_to_one(
        "Slider",
        backref="images",
        lazy="joined",
        innerjoin=True
    )


class Menu(Slugger, SurrogatePK, Base):

    __tablename__ = u'tb_menu'

    label = Column(Unicode(100))
    name = Column('route_name', Unicode(100))
    url = Column('route_url', Unicode(200))

    groups = relation(
        "Group",
        backref="menu",
        secondary="grp_menu"
    )

    def __init__(self, label, name, url):
        self.label = label
        self.name = name
        self.slug = name
        self.url = url


class GroupMenu(Base):

    __tablename__ = u'grp_menu'

    menu_id = Column(CHAR(10), ForeignKey('tb_menu.id'), primary_key=True)
    group_id = Column(CHAR(10), ForeignKey('tb_grp.id'), primary_key=True)
