"""
 # Copyright (c) 03 2015 | surya
 # 23/03/15 nanang.ask@kubuskotak.com
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
 #  api.py
"""
import logging

from decorator import decorator
from niimanga.libs.utils import genid


LOG = logging.getLogger(__name__)


class api_token(object):
    """View decorator to set check the client is permitted

    Since api calls can come from the api via a api_key or a logged in user via
    the website, we need to check/authorize both

    If this is an api call and the api key is valid, stick the user object
    found onto the request.user so that the view can find it there in one
    place.

    """

    def __init__(self, api_field, user_fetcher, admin_only=False, anon=False):
        """
        :param api_field: the name of the data in the request.params and the
                          User object we compare to make sure they match
        :param user_fetcher: a callable that I can give a username to and
                             get back the user object

        :sample: @ApiAuth('api_key', UserMgr.get)

        """
        self.api_field = api_field
        self.user_fetcher = user_fetcher
        self.admin_only = admin_only
        self.anon = anon

    def __call__(self, action_):
        """ Return :meth:`wrap_action` as the decorator for ``action_``. """
        return decorator(self.wrap_action, action_)

    def _check_api_key(self, request):
        """If admin only, verify current api belongs to an admin user"""
        api_key = request.params.get(self.api_field, None)

        if request.user is None:
            user = self.user_fetcher(api_key=api_key)
        else:
            user = request.user

        if user is not None and user.is_admin:
            request.user = user
            return True

    def wrap_action(self, action_, *args, **kwargs):
        """
        Wrap the controller action ``action_``.

        :param action_: The controller action to be wrapped.

        ``args`` and ``kwargs`` are the positional and named arguments which
        will be passed to ``action_`` when called.

        """
        # cek api_key jika ditemukan di storage return true
        print(genid())
        # request should be the one and only arg to the view function
        request = args[0].R
        api_key = request.matchdict.get(self.api_field, None)

        # if this is admin only, you're either an admin or not
        if self.admin_only:
            if self._check_api_key(request):
                return action_(*args, **kwargs)
            else:
                request.response.status_int = 403
                return {'error': "Not authorized for request."}

        # get the user the api key belongs to
        if self.api_field in request.params:
            # we've got a request with url params
            api_key = request.params.get(self.api_field, None)

        def is_json_auth_request(request):
            if hasattr(request, 'json_body'):
                if self.api_field in request.json_body:
                    return True
            return False

        if is_json_auth_request(request):
            # we've got a ajax request with post data
            api_key = request.json_body.get(self.api_field, None)

        if api_key is not None:
            # now get what this user should be based on the api_key
            request.user = self.user_fetcher(api_key=api_key)

            # if there's a username in the url (rdict) then make sure the user
            # the api belongs to is the same as the url. You can't currently
            # use the api to get info for other users.
            if request.user and request.user.api_key == api_key:
                return action_(*args, **kwargs)

        # if this api call accepts anon requests then let it through
        if self.anon:
            return action_(*args, **kwargs)

        # otherwise, we're done, you're not allowed
        request.response.status_int = 403
        return {'error': "Not authorized for request."}