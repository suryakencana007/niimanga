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
 #  errorhandling.py
"""
from pyramid.httpexceptions import HTTPUnauthorized


class AuthErrorHandling(object):
    @staticmethod
    def error_invalid_request():
        """
        The request is missing a required parameter, includes an
        unsupported parameter or parameter value, repeats a
        parameter, includes multiple credentials, utilizes more
        than one mechanism for authenticating the client, or is
        otherwise malformed.
        """
        return dict(error='invalid_request',
                    error_description="")

    @staticmethod
    def error_invalid_client():
        """
        Client authentication failed (e.g. unknown client, no
        client authentication included, multiple client
        authentications included, or unsupported authentication
        method). The authorization server MAY return an HTTP 401
        (Unauthorized) status code to indicate which HTTP
        authentication schemes are supported. If the client
        attempted to authenticate via the "Authorization" request
        header field, the authorization server MUST respond with
        an HTTP 401 (Unauthorized) status code, and include the
        "WWW-Authenticate" response header field matching the
        authentication scheme used by the client.
        """
        return dict(error='invalid_client',
                    error_description="")

    @staticmethod
    def error_invalid_grant():
        """
        The provided authorization grant is invalid, expired,
        revoked, does not match the redirection URI used in the
        authorization request, or was issued to another client.
        """
        return dict(error='invalid_grant',
                    error_description="")

    @staticmethod
    def error_unauthorized_client():
        """
        The authenticated client is not authorized to use this
        authorization grant type.
        """
        return dict(error='unauthorized_client',
                    error_description="")

    @staticmethod
    def error_unsupported_grant_type():
        """
        The authorization grant type is not supported by the
        authorization server.
        """
        return dict(error='unsupported_grant_type',
                    error_description="")

    @staticmethod
    def error_invalid_scope():
        """
        The requested scope is invalid, unknown, malformed, or
        exceeds the scope granted by the resource owner.
        """
        return dict(error='invalid_scope',
                    error_description="")

    @staticmethod
    def error_invalid_token(token_type):
        """
        The specific handling of this error is based on the token
        type used, i.e. bearer or MAC.
        """
        raise HTTPUnauthorized('todo') # TODO: add correct error handling for bearer