"""
 # Copyright (c) 05 2015 | surya
 # 18/05/15 nanang.ask@kubuskotak.com
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
 #  __init__.py.py
"""
import urlparse

from niimanga.libs.exceptions import HtmlError
from requests import request


class Site:
    def __init__(self):
        pass

    def get_html(self, url, method='GET', **kwargs):
        resp = request(method, url, **kwargs)
        if resp.status_code != 200:
            raise HtmlError({'msg': 'external_request_fail', 'url': url})
        return resp.content

    def fetch_manga_seed_page(self, url, **kwargs):
        return self.get_html(url, **kwargs)

    def fetch_chapter_seed_page(self, url, **kwargs):
        return self.get_html(url, **kwargs)

    def fetch_page_image(self, url, **kwargs):
        return self.get_html(url, **kwargs)

    def search_by_author(self, author):
        """
        Return list of chapter dicts whose keys are:
            name
            url
            site

        This should be specifically implemented in each Site subclass. If not,
        this method will be used which returns an empty list.
        """
        return []

from mangaeden import MangaEden
from batoto import Batoto

available_sites = [
    # Kissmanga(),
    # Vitaku(),
    Batoto(),
    # Mangafox(),
    # Mangahere(),
    # MangaHereMob(),
    MangaEden()
]


# Factory function, return instance of suitable "site" class from url
def get_site(url):
    netloc = urlparse.urlparse(url).netloc

    for site in available_sites:
        if netloc in site.netlocs:
            return site
    return None