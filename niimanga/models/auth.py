"""
 # Copyright (c) 02 2015 | surya
 # 27/02/15 nanang.ask@kubuskotak.com
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
 #  auth.py
"""
import hashlib
import logging
from datetime import timedelta, datetime

import bcrypt
from niimanga.libs.utils import nonce, hmacsha256, CLIENT_KEY_LENGTH, CLIENT_SECRET_LENGTH
from niimanga.models import Base, DBSession
from niimanga.models.acl import Group
from niimanga.models.meta.schema import SurrogatePK
from sqlalchemy import Column, Integer, ForeignKey, Unicode, DateTime, Boolean, CHAR
from sqlalchemy.orm import relation, synonym


LOG = logging.getLogger(__name__)
ACTIVATION_AGE = timedelta(days=4)


class ActivationMgr(object):

    @staticmethod
    def count():
        """Count how many activations are in the system."""
        return Activation.query.count()

    @staticmethod
    def get_user(username, code):
        """Get the user for this code"""
        qry = Activation.query. \
            filter(Activation.code == code). \
            filter(User.username == username)

        res = qry.first()

        if res is not None:
            return res.user
        else:
            return None

    @staticmethod
    def get_user_by(email, code):
        """Get the user for this code by email"""

        qry = Activation.query. \
            filter(Activation.code == code). \
            filter(User.email == email)

        res = qry.first()

        if res is not None:
            return res.user
        else:
            return None

    @staticmethod
    def activate_user(username, code, new_pass):
        """Given this code get the user with this code make sure they exist"""

        qry = Activation.query. \
            filter(Activation.code == code). \
            filter(User.username == username)

        res = qry.first()

        if UserMgr.acceptable_password(new_pass) and res is not None:
            user = res.user
            user.is_activated = True

            user.password = new_pass
            res.activate()

            LOG.debug(dict(user))

            return True
        else:
            return None


class Activation(Base):
    """Handle activations/password reset items for users

    The id is the user's id. Each user can only have one valid activation in
    process at a time

    The code should be a random hash that is valid only one time
    After that hash is used to access the site it'll be removed

    The created by is a system: new user registration, password reset, forgot
    password, etc.

    """
    __tablename__ = u'activations'

    id = Column(CHAR(10), ForeignKey('tb_usr.id'), primary_key=True)
    code = Column(Unicode(60))
    valid_until = Column(
        DateTime,
        default=lambda: datetime.utcnow + ACTIVATION_AGE)
    created_by = Column('created_by', Unicode(255))

    def __init__(self, created_system):
        """Create a new activation"""
        self.code = Activation._gen_activation_hash()
        self.created_by = created_system
        self.valid_until = datetime.utcnow() + ACTIVATION_AGE

    @staticmethod
    def _gen_activation_hash():
        """Generate a random activation hash for this user account"""
        # for now just cheat and generate an api key, that'll work for now
        return hmacsha256(User.gen_api_key(), 'sekrit')[:60]

    def activate(self):
        """Remove this activation"""
        DBSession.delete(self)


class UserMgr(object):
    """ Wrapper for static/combined operations of User object"""

    @staticmethod
    def count():
        """Number of users in the system."""
        return User.query.count()

    @staticmethod
    def get_list(active=None, order=None, limit=None):
        """Get a list of all of the user accounts"""
        user_query = User.query.order_by(User.username)

        if active is not None:
            user_query = user_query.filter(User.activated == active)

        if order:
            user_query = user_query.order_by(getattr(User, order))
        else:
            user_query = user_query.order_by(User.signup)

        if limit:
            user_query = user_query.limit(limit)

        return user_query.all()

    @staticmethod
    def get(user_id=None, username=None, email=None, api_key=None):
        """Get the user instance for this information

        :param user_id: integer id of the user in db
        :param username: string user's name
        :param inactive: default to only get activated true

        """
        user_query = User.query

        if username is not None:
            return user_query.filter(User.username == username).first()

        if user_id is not None:
            return user_query.filter(User.id == user_id).first()

        if email is not None:
            return user_query.filter(User.email == email).first()

        if api_key is not None:
            return user_query.filter(User.api_key == api_key).first()

        return None

    # TODO: Untuk proses access control list per group user
    @staticmethod
    def auth_groupfinder(userid, request):
        """Pyramid wants to know what groups a user is in

        We need to pull this from the User object that we've stashed in the
        request object

        """
        user = request.user
        if user is not None:
            if user.is_admin:
                return 'admin'
            else:
                return 'user'
        return None

    @staticmethod
    def acceptable_password(password):
        """Verify that the password is acceptable

        Basically not empty, has more than 3 chars...

        """
        LOG.debug("PASS")
        LOG.debug(password)

        if password is not None:
            LOG.debug(len(password))

        if password is None:
            return False

        if len(password) < 3:
            return False

        return True

    @staticmethod
    def signup_user(email, signup_method, allowed_scopes=[]):
        # Get this invite party started, create a new user acct.
        new_user = User()
        new_user.email = email
        new_user.username = email
        new_user.invited_by = signup_method
        new_user.api_key = User.gen_api_key()
        new_user.secret = User.gen_secret()
        new_user.set_scopes(allowed_scopes)

        # they need to be deactivated
        new_user.reactivate('invite')

        # decrement the invite counter
        DBSession.add(new_user)
        return new_user


class User(SurrogatePK, Base):
    """Basic Tabel User"""
    __tablename__ = u'tb_usr'

    # id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(255))
    username = Column(Unicode(255), unique=True)
    email = Column(Unicode(255), unique=True)
    _password = Column('password', Unicode(60))

    # set for authorization
    api_key = Column(Unicode(CLIENT_KEY_LENGTH), unique=True)
    secret = Column(Unicode(CLIENT_SECRET_LENGTH))
    """scopes delimited"""
    allowed_scopes = Column(Unicode(256))

    last_login = Column(DateTime)
    is_activated = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    invite_ct = Column(Integer, default=0)
    invited_by = Column('invited_by', Unicode(255))

    # tokens = one_to_many("ClientToken", backref="client")

    activation = relation(
        Activation,
        cascade="all, delete, delete-orphan",
        uselist=False,
        backref='user'
    )

    groups = relation(
        Group,
        secondary='grp_usr'
    )

    def __init__(self):
        """By Default a user start disabled activade"""
        self.activation = Activation('signup')
        self.is_activated = False

    def set_scopes(self, allowed_scopes=[]):
        """Sets the scopes/ Principal ACL allowed by the client."""
        self.allowed_scopes = ' '.join(allowed_scopes)

    def get_scopes(self):
        """Get list semua scopes / principal ACL"""
        return self.allowed_scopes.split(' ')

    def check_secret(self, secret):
        """Cek validasi secret dari client"""
        return str(secret) == self.secret

    def _set_password(self, password):
        """Hash password on the fly"""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        # Hash a password for the first time, with a randomly-generated salt\
        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(password_8bit, salt)

        # Make sure the hashed password is an UTF-8 object at the of
        # the process because SQLAlchemy _wants_ a unicode object for Unicode
        # fields
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the password hashed"""
        return self._password
    """it's cool alias routed"""
    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.

        """
        # the password might be null as in the case of morpace employees
        # logging in via ldap. We check for that here and return them as an
        # incorrect login
        if self.password:
            salt = self.password[:29]
            return self.password == bcrypt.hashpw(password, salt)
        else:
            return False

    def safe_data(self):
        """Return safe data to be sharing around"""
        hide = ['_password', 'password', 'is_admin', 'api_key']
        return dict(
            [(k, v) for k, v in dict(self).iteritems() if k not in hide]
        )

    def deactivate(self):
        """In case we need to disable the login"""
        self.is_activated = False

    def reactivate(self, creator):
        """Put the account through the reactivation process

        This can come about via a signup or from forgotten password link

        """
        # if we reactivate then reinit this
        self.activation = Activation(creator)
        self.is_activated = False

    def has_invites(self):
        """Does the user have any invitations left"""
        return self.invite_ct > 0

    def invite(self, email):
        """Invite a user"""
        if not self.has_invites():
            return False
        if not email:
            raise ValueError('You must supply an email address to invite')
        else:
            # get this invite party started, create a new useracct
            new_user = UserMgr.signup_user(email, self.username)

            # decrement the invite counter
            self.invite_ct -= 1
            DBSession.add(new_user)
            return new_user

    @staticmethod
    def gen_secret():
        return nonce(CLIENT_SECRET_LENGTH)

    @staticmethod
    def gen_api_key():
        """Generate api key dari client ID + hash """
        while True:
            m = hashlib.sha256()
            m.update(nonce(CLIENT_KEY_LENGTH))
            key = str(m.hexdigest()[:CLIENT_KEY_LENGTH])
            if not User.query.filter(User.api_key == key).count():
                return key

