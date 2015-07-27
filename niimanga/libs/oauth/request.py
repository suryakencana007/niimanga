"""
 # Copyright (c) 04 2015 | surya
 # 06/04/15 nanang.ask@kubuskotak.com
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
 #  request.py
"""
import binascii
import logging
from pyramid.request import Request

LOG = logging.getLogger(__name__)


class RequestOAuth(Request):
    """
    Proxy Class extending a request with information necessary for
    """
    def __init__(self, request):
        self.__subject = request
        # Add OAuth related information from the header to params
        self.authentication = self._get_basic_authentication_credentials(request)
        self.access_token = self._get_access_token(request)

    def __getattr__(self, name):
        return getattr(self.__subject, name)

    def _get_access_token(self, request):
        """
        Retrieves the access token and the token type from the Authentication
        header and stores it in a dictionary.
        """
        if not hasattr(request, 'authorization') or request.authorization is None:
            return None

        try:
            auth_method, information = request.authorization
        except ValueError: # not enough values to unpack
            return None

        if auth_method.lower() == 'bearer':
            token = information.strip()
            return dict(type='bearer',
                        token=token)
        elif auth_method.lower() == 'mac':
            raise NotImplementedError()
        return None

    def _get_basic_authentication_credentials(self, request):
        """
        Retrieves the user id and password from the Authentication header and
        stores it in a dictionary.
        """
        if not hasattr(request, 'authorization') or request.authorization is None:
            return None

        try:
            auth_method, auth = request.authorization
        except ValueError: # not enough values to unpack
            return None

        if auth_method.lower() == 'basic':
            try:
                # auth = auth.strip().decode('base64')
                auth = auth.strip()
                LOG.debug(auth)
            except binascii.Error as bin: # Decode is not possible
                LOG.debug("{0} error biascii".format(bin.message))
                return None
            try:
                key, secret = auth.split(':', 1)
            except ValueError as val: # not enough values to unpack
                LOG.debug(val.message)
                return None
            return dict(type='basic',
                        client_key=unicode(key.strip()),
                        client_secret=unicode(secret.strip()))
        return None