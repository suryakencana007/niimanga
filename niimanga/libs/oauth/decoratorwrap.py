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
 #  decorator.py
"""
import logging

from decorator import decorator
from niimanga.libs.oauth.request import RequestOAuth
from niimanga.libs.utils import ResponseHTTP
from niimanga.models.authz import TokenManager


LOG = logging.getLogger(__name__)


class tokenizer(object):
    """View decorator to set check the client is permitted

    Since api calls can come from the api via a api_key or a logged in user via
    the website, we need to check/authorize both

    If this is an api call and the api key is valid, stick the user object
    found onto the request.user so that the view can find it there in one
    place.

    """

    def __init__(self, token_field, user_fetcher, allowed_scopes=[], anon=False):
        """
        :param api_field: the name of the data in the request.params and the
                          User object we compare to make sure they match
        :param user_fetcher: a callable that I can give a username to and
                             get back the user object
        :param allowed_scopes: USer scope for access allowed token

        :sample: @ApiAuth('api_key', UserMgr.get)

        """
        self.token_field = token_field
        self.user_fetcher = user_fetcher
        self.allowed_scopes = allowed_scopes
        self.anon = anon

    def __call__(self, action_):
        """ Return :meth:`wrap_action` as the decorator for ``action_``. """
        return decorator(self.wrap_action, action_)

    def wrap_action(self, action_, *args, **kwargs):
        """
        Wrap the controller action ``action_``.

        :param action_: The controller action to be wrapped.

        ``args`` and ``kwargs`` are the positional and named arguments which
        will be passed to ``action_`` when called.

        """
        try:
            # get token
            # from header information
            request = RequestOAuth(args[0].R)
            with ResponseHTTP(response=request.response) as t:
                _in = u'Failed'
                # handle token
                token = request.access_token

                if token:
                    oauth_context = TokenManager.get_token_context(token.get('token'))
                    if oauth_context.valid:
                        args[0].__dict__.update(R=request)
                        kwargs.update(dict(oauth_context=oauth_context))
                        # not mandatory use of oauth, but valid token
                        if self.anon:
                            LOG.debug(oauth_context.valid)
                            return action_(*args, **kwargs)
                        # validate scope
                        elif TokenManager.has_valid_scope(oauth_context.scopes, self.allowed_scopes):
                            LOG.debug(oauth_context.scopes)
                            # kwargs.update(dict(oauth_context=oauth_context))
                            return action_(*args, **kwargs)
                else:
                    if self.anon:
                        return action_(*args, **kwargs)

                # api_key = request.matchdict.get(self.api_field, None)

                # otherwise, we're done, you're not allowed
                message = 'Not authorized for request.'
                code, status = ResponseHTTP.FORBIDDEN
            return t.to_json(_in,
                             message=message,
                             code=code, status=status)
        except ValueError as e:
            LOG.debug(e.message)