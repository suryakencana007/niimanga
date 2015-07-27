"""
 # Copyright (c) 03 2015 | surya
 # 24/03/15 nanang.ask@kubuskotak.com
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
 #  authz.py
"""
import logging
import datetime

from niimanga.libs.exceptions import ClientNotFoundError
from niimanga.libs.utils import ACCESS_TOKEN_LENGTH, REFRESH_TOKEN_LENGTH, nonce
from niimanga.models import Base, DBSession
from niimanga.models.auth import User
from niimanga.models.meta.schema import SurrogatePK
from sqlalchemy import Column, Unicode, DateTime


LOG = logging.getLogger(__name__)


class TokenManager(object):
    @staticmethod
    def get_token_context(token):
        """returns information about the token"""
        token_info = ClientToken.query.filter(ClientToken.token == token).first()
        context = TokenContext()
        if token_info:
            valid = not token_info.expired() and not token_info.is_revoked()
            context.scopes = token_info.get_scopes()
            context.client_id = token_info.client.id
            context.valid = valid
            LOG.debug("TOKEN INFO: {0}".format(valid))
        else:
            LOG.debug("TOKEN FALSE")
            context.valid = False
        return context

    @staticmethod
    def get_client_by_id(id):
        client = User.query.get(id)
        if not client:
            raise ClientNotFoundError
        return client

    @staticmethod
    def get_client_by_key(key):
        client = User.query.filter(User.api_key == key).first()
        if not client:
            raise ClientNotFoundError
        return client

    @staticmethod
    def is_valid_access_token(token, allowed_scopes):
        """Checks the validity of the access token."""
        # Retrieve token information
        token_info = ClientToken.query.filter(ClientToken.token == token).first()
        if token_info and not token_info.expired():
            # look for correct scope
            for token_scope in token_info.get_scopes():
                # correct scope found
                if token_scope in allowed_scopes:
                    return True, token_info.client.id, token_scope

        # Bad token
        return False, None, None
    # TODO system scopes

    @staticmethod
    def authenticate(key, secret):
        """Tries to authenticate a client using its key and secret

        Returns tuple (boolean, integer): true and the client_id if successful
        else false and None
        """
        try:
            client = TokenManager.get_client_by_key(key)
        except ClientNotFoundError:
            print("No client found with key: %s" % key)
            return False, None
        else:
            if client.check_secret(secret):
                return True, client.id
            print type(secret)
            print type(client.secret)
            print("Secret '%s' did not match '%s'" % (secret, client.secret))
            return False, None

    @staticmethod
    def can_request_scope(client_id, requested_scopes=[]):
        """Checks if the requested scope can be granted to the client"""
        try:
            client = TokenManager.get_client_by_id(client_id)
        except ClientNotFoundError:
            return False
        else:
            # verify requested scopes
            for requested_scope in requested_scopes:
                if not requested_scope in client.allowed_scopes:
                    # scope was not allowed
                    return False
            # all scopes were allowed
            return True

    @staticmethod
    def issue_access_token(client_id, allowed_scopes=[], refreshable=False):
        """Issues an access token to the client"""
        access_token = ClientToken(refreshable)
        access_token.set_scopes(allowed_scopes)
        client = TokenManager.get_client_by_id(client_id)
        access_token.client = client
        # Increment granted client tokens
        # client.tokens_granted += 1

        DBSession.add(access_token)
        DBSession.flush()
        return access_token

    @staticmethod
    def has_valid_scope(scopes, allowed_scopes):
        for token_scope in scopes:
            if token_scope in allowed_scopes:
                return True
        return False


class TokenContext(object):
    def __init__(self):
        self.scopes = None
        self.client_id = None
        self.valid = False


class ClientToken(SurrogatePK, Base):
    """Tabel Client Token """

    __tablename__ = u'client_token'

    token = Column(Unicode(ACCESS_TOKEN_LENGTH), unique=True)
    refresh_token = Column(Unicode(REFRESH_TOKEN_LENGTH))
    allowed_scopes = Column(Unicode(255))
    issued_at = Column(DateTime)
    expires_at = Column(DateTime)
    revoked_at = Column(DateTime)

    def __init__(self, refreshable=True, expires_in=30, allowed_scope=[]):
        self.allowed_scopes = ' '.join(allowed_scope)
        # Generate Access Token
        self.token = self._generate_token(ACCESS_TOKEN_LENGTH)
        # Generate Refresh Token
        if refreshable:
            self.refresh_token = self._generate_token(REFRESH_TOKEN_LENGTH)
        # Expiration
        timedelta = datetime.timedelta(days=expires_in)
        self.issued_at = datetime.datetime.now()
        self.expires_at = self.issued_at + timedelta

    def revoke(self):
        """Revoke this token so it can not be used for authenticating
        a client."""
        self.revoked_at = datetime.datetime.now()

    def is_revoked(self):
        """Checks whether the access token is revoked."""
        return self.revoked_at is not None

    def expired(self):
        """Returns ``True`` if the datetime from ``expires_at`` is in the past,
        relative to the server's time or it has been revoked."""
        return self.is_revoked() or self.expires_at < datetime.datetime.now()

    def set_scopes(self, scopes):
        if scopes:
            self.allowed_scopes = " ".join(scopes)
        else:
            self.allowed_scopes = ""

    def get_scopes(self):
        """Returns a list of all scopes allowed by the access token."""
        return self.allowed_scopes.split(' ')

    def confirm_authorized_scopes(self, scopes):
        """Validates if the requested scopes are allowed by the access token."""
        allowed_scopes = self.get_scopes()
        for scope in scopes:
            if not scope in allowed_scopes:
                return False
        return True

    def _generate_token(self, length=ACCESS_TOKEN_LENGTH):
        token = self._generate_random_token(length=length)
        while self._exists_already(token):
            token = self._generate_random_token(length=length)
        return token

    def _generate_random_token(self, length):
        return nonce(length)

    def _exists_already(self, key):
        q = ClientToken.query.filter(ClientToken.token == key)
        return q.count() > 0

