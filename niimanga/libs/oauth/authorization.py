"""
 # Copyright (c) 03 2015 | surya
 # 31/03/15 nanang.ask@kubuskotak.com
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
 #  authorization.py
"""

import logging

from niimanga.libs.oauth.errorhandling import AuthErrorHandling
from niimanga.models.authz import TokenManager
import transaction

LOG = logging.getLogger(__name__)


def validate_access_token(access_token, allowed_scopes):
    return TokenManager.is_valid_access_token(access_token, allowed_scopes)


def get_token_context(token):
    return TokenManager.get_token_context(token)


def client_credentials_authorization(auth_credentials, scopes=[]):
    """
    The client can request an access token using only its client
    credentials (or other supported means of authentication) when the
    client is requesting access to the protected resources under its
    control, or those of another resource owner which has been previously
    arranged with the authorization server (the method of which is beyond
    the scope of this specification).

    The client credentials grant type MUST only be used by private
    clients.

    +---------+                                  +---------------+
    |         |                                  |               |
    |         |>--(A)- Client Authentication --->| Authorization |
    | Client  |                                  |    Server     |
    |         |<--(B)---- Access Token ---------<|               |
    |         |                                  |               |
    +---------+                                  +---------------+

                 Figure 6: Client Credentials Flow


    The flow illustrated in Figure 6 includes the following steps:

    (A)  The client authenticates with the authorization server and
         requests an access token from the token endpoint.
    (B)  The authorization server authenticates the client, and if valid
         issues an access token.

    Authorization Request and Response
    ----------------------------------

    Since the client authentication is used as the authorization grant,
    no additional authorization request is needed.
    """

    # Authentication
    LOG.debug("Starting client_credentials workflow")
    LOG.debug("Requested scopes: %s" % scopes)

    if auth_credentials is None:
        return AuthErrorHandling.error_unauthorized_client()

    authenticated, client_id = TokenManager.authenticate(auth_credentials.get('client_key'),
                                                         auth_credentials.get('client_secret'))
    if authenticated:
        # Validate allowed
        allowed = TokenManager.can_request_scope(client_id, scopes)
        LOG.debug(allowed)
        if allowed:
            LOG.debug("Authentication allowed, issueing token.")
            access_token = TokenManager.issue_access_token(client_id=client_id,
                                                           allowed_scopes=scopes,
                                                           refreshable=False)
            response = dict(access_token=access_token.token,
                            token_type="bearer",
                            expires_in=access_token.expires_at.isoformat())
            transaction.commit()
            return response
        else:
            LOG.debug("One or more scopes were not allowed: %s" % scopes)
            # Scope was not allowed
            return AuthErrorHandling.error_invalid_scope()
    else:
        LOG.debug("Client is not authorized to ask tokens.")
        # Client not authorized
        return AuthErrorHandling.error_unauthorized_client()