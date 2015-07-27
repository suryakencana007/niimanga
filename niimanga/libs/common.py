"""
 # Copyright (c) 06 2015 | surya
 # 18/06/15 nanang.ask@kubuskotak.com
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
 #  common.py
"""
import os


def crawlable(func):
    """
    Render crawler-friendly html to serve search engine and Open Graph bots.
    If requester is an actual browser, simply serve the client app's static
    html.
    """
    def wrapped(handler, query=None):
        # If requester is a bot, serve custom "bot version"
        # crawlers = ('Googlebot', 'facebookexternalhit', 'Slackbot')
        # for crawler in crawlers:
        #     if crawler in handler.headers['User-Agent']:
        #         return func(handler, query)

        print(os.getcwd())
        # Not a bot. Let's serve the js app!
        with open(os.getcwd() + '/frontends/public/index.html', 'r') as f:
            html = f.read()
        handler.response.write(html)
        return None

    return wrapped