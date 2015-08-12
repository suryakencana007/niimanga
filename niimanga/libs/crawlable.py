"""
 # Copyright (c) 08 2015 | surya
 # 11/08/15 nanang.ask@kubuskotak.com
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
 #  crawlable.py
"""
import logging
import os

from decorator import decorator


LOG = logging.getLogger(__name__)


class CrawlAble(object):
    """
    View decorator to set check client agent browser

    Render crawler-friendly html to serve search engine and Open Graph bots.
    If requester is an actual browser, simply serve the client app's static
    html.
    """

    def __init__(self):
        pass

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
        # request should be the one and only arg to the view function
        request = args[0].R

        # If requester is a bot, serve custom "bot version"
        crawlers = ('Googlebot', 'facebookexternalhit', 'Slackbot')
        for crawler in crawlers:
            if crawler in request.headers['User-Agent']:
                return action_(*args, **kwargs)

        # Not a bot. Let's serve the js app!
        with open(os.getcwd() + '/niimanga/public/index.html', 'r') as f:
            request.response.content_type = 'text/html'
            request.response.charset = 'UTF-8'
            request.response.status_int = 200
            request.response.body = f.read()
        LOG.info('dari crawlable decorated123')
        return request.response
        # return action_(*args, **kwargs)
