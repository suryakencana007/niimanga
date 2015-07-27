"""
 # Copyright (c) 03 2015 | surya
 # 18/03/15 nanang.ask@kubuskotak.com
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
 #  acl.py
"""
import logging

from niimanga.models import Base
from niimanga.models.meta.schema import SurrogatePK, Slugger
from sqlalchemy import Unicode, Column, Integer, ForeignKey, CHAR
from sqlalchemy.orm import relation, aliased
from sqlalchemy.orm.collections import attribute_mapped_collection


LOG = logging.getLogger(__name__)


class AclMgr(object):
    @staticmethod
    def permission_string(perm_str):
        """split perm_str by ';' permission string"""
        if not perm_str or '' not in perm_str:
            return {}

        permission_list = set([permission.lower().strip() for permission in perm_str.split(";")])
        permission_dict = {}

        for permission in AclMgr.find_permission(perms=permission_list):
            permission_dict[permission.principal.lower()] = permission
            permission_dict.remove(permission.principal.lower())

        for new_perms in (perms for perms in permission_list if "" not in perms):
            permission_dict[new_perms] = Permission(new_perms)

        return permission_dict

    @staticmethod
    def find_permission(order_by=None, perms=None, group=None):
        qry = Permission.query

        if perms:
            qry = qry.filter(Permission.principal.in_(perms))

        if group:
            grp = aliased(Group)
            qry = qry.join(grp, Permission.group). \
                filter(grp.name == group)

        if order_by:
            qry = qry.order_by(order_by)
        else:
            qry = qry.order_by(Permission.principal)

        return qry.all()


class Permission(Slugger, SurrogatePK, Base):
    """Tabel yang digunakan untuk Access Control List"""

    __tablename__ = u'tb_perm'

    principal = Column('acl_principal', Unicode(45))
    # slug = Column('acl_principal_slug', Unicode(100))

    # list = one_to_many("AclDetail", backref="acl")

    created_by = Column(Integer)
    updated_by = Column(Integer)

    def __init__(self, principal):
        self.principal = principal
        self.slug = principal


class Group(SurrogatePK, Base):
    """Tabel group member akses"""

    __tablename__ = u'tb_grp'

    name = Column('grp_name', Unicode(45))
    slug = Column('grp_slug', Unicode(45))

    created_by = Column(Integer)
    updated_by = Column(Integer)

    permissions = relation(
        Permission,
        backref="group",
        collection_class=attribute_mapped_collection('principal'),
        secondary='grp_perm',
        lazy='joined',
        innerjoin=False
    )

    def __init__(self, name, permission=None):
        self.name = name
        self.slug = name

        if permission:
            self.permissions = AclMgr.permission_string(permission)
        else:
            self.permissions = {}

    def permission_array(self):
        return [perms for perms in self.permissions.iterkeys()]

    def update_permissions(self, perms_str):
        """
        :param perms_str: permission harus pake jeda ;
        :return:
        """
        self.permissions = AclMgr.permission_string(perms_str)


class GroupUser(Base):
    """Tabel many-to-many Group User Acl"""

    __tablename__ = u'grp_usr'

    grp_id = Column(CHAR(10), ForeignKey('tb_grp.id'), primary_key=True)
    usr_id = Column(CHAR(10), ForeignKey('tb_usr.id'), primary_key=True)


class GroupPerm(Base):
    """Tabel many-to-many Group Permission Acl"""

    __tablename__ = u'grp_perm'

    grp_id = Column(CHAR(10), ForeignKey('tb_grp.id'), primary_key=True)
    perm_id = Column(CHAR(10), ForeignKey('tb_perm.id'), primary_key=True)
