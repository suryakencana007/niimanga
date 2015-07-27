"""
 # Copyright (c) 05 2015 | surya
 # 14/05/15 nanang.ask@kubuskotak.com
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
 #  mmangahere.py
"""
import logging

from bs4 import BeautifulSoup
from natsort import natsorted
from niimanga.libs.exceptions import HtmlError
from niimanga.sites import Site
import re
import requests
from requests_futures.sessions import FuturesSession


LOG = logging.getLogger(__name__)


class MangaHereMob(Site):

    netlocs = ['m.mangahere.co', 'mangahere']

    def search_genre(self, category):
        url = 'http://m.mangahere.co/directory/' + category
        return self._series_list(url, type='search')

    def list_genre(self, keyword=None):
        url = 'http://m.mangahere.co/directory/'
        resp = requests.get(url)
        if resp.status_code != 200:
            return []
        soup = BeautifulSoup(resp.content)
        ul = soup.find_all('ul', class_='genres-list')

        list_genres = []
        for ul in ul:
            list_genres.extend([{'name': li.text,
                                 'url': re.search(r'/directory/(.*)/', li.find('a').attrs['href']).group(1)}
                                for li in ul.find_all('li')])
        return list_genres

    def search_hot(self, keyword):
        url = 'http://m.mangahere.co/hot'
        return self._series_list(url, type='hot')

    def search_by_author(self, author):
        url = 'http://m.mangahere.co/author/' + author
        return self._series_list(url, type='search')

    def search_latest(self, keyword):
        url = 'http://m.mangahere.co'
        return self._series_list(url, type='latest')

    def search_series(self, keyword):
        url = 'http://m.mangahere.co/search?'
        params = {
            'query': keyword
        }
        return self._series_list(url, params, type='search')

    def _normalize_chapter_href(self, href):
        return href.replace('/manga', '/roll_manga')

    def series_info(self, html):
        soup = BeautifulSoup(html)
        chapters = self._chapters(soup)
        thumb_url = self._thumbnail_url(soup)
        tags = self._tags(soup)
        name = self._name(soup)
        status = self._status(soup)
        description = self._description(soup)
        authors = self._authors(soup)
        return {
            'site': self.netlocs[0],
            'chapters': chapters,
            'thumb_url': thumb_url,
            'tags': tags,
            'name': name,
            'status': status,
            'description': description,
            'authors': authors,
            }

    def _chapters(self, soup):
        table = soup.find('div', class_='manga-chapters').find_all('a')

        return [{'url': a.attrs['href'],
                 'name': a.string.strip()}
                for a in table]

    def _thumbnail_url(self, soup):
        divdetail = soup.find('div', class_='manga-detail-top')
        return divdetail.find('img')['src']

    def _tags(self, soup):
        tags = soup.find('div', class_='manga-genres').find_all('a')

        return [{'tag': tag.text.strip(),
                 'url': re.search(r'/directory/(.*)/', tag.attrs['href']).group(1)} for tag in tags]

    def _name(self, soup):
        # <link rel='alternate' title='Naruto manga' ...
        # => must remove the ' manga' part
        return soup.find('div', class_='manga-detail-top').find('p').text.strip()

    def _status(self, soup):
        status_span = soup.find('div', class_='detail-info').find_all('p')
        return status_span[1].text.strip().lower()

    def _description(self, soup):
        desc_span = soup.find('div', class_='manga-summary')
        # desc = [s.text for s in p_tags if type(s) == bs4.element.Tag]
        desc = desc_span.text.split('\r\n')
        description = [d.strip() for d in desc]
        return description

    def _authors(self, soup):
        detail_info = soup.find('div', class_='detail-info').find_all('p')
        authors = detail_info[0].find_all('a')

        return [text.text.replace('Status:', '') for text in authors if text.text is not '']

    # Chapter data
    # - name "Naruto Ch.101"
    # - pages [url1, url2, ...] - in ascending order
    # - prev_chapter_url
    # - next_chapter_url
    # - series_url
    def chapter_info(self, html, **kwargs):
        # ambil yg versi mobile
        print(kwargs['url'])
        soup = BeautifulSoup(html)
        name = self._chapter_name(soup)
        series_url = self._chapter_series_url(kwargs['url'])
        if 'roll_manga' in kwargs['url']:
            prev, next = self._chapter_prev_next(soup)
            pages = self._chapter_roll_pages(soup, html, kwargs['url'])
        else:
            prev, next = None, None
            pages = self._chapter_pages(soup, html, kwargs['url'])

        return {
            'name': name,
            'pages': pages,
            'series_url': series_url,
            'next_chapter_url': next,
            'prev_chapter_url': prev,
            }

    def _chapter_prev_next(self, soup):
        prev, next = None, None
        div = soup.find('div', class_='roll-pagebtn')

        prev_a = div.find_all('a', text='Prev Chapter', limit=1)
        LOG.info(prev_a)
        if len(prev_a) > 0:
            prev = prev_a[0].attrs['href']

        # next_p = div[1] if len(div) > 1 else None
        next_p = div.find_all('a', text='Next Chapter', limit=1)
        if len(next_p) > 0:
            next = next_p[0].attrs['href']
        return prev, next

    def _chapter_name(self, soup):
        divdetail = soup.find('div', class_='return-title')
        LOG.info(divdetail)
        return divdetail.text.strip()

    def _chapter_roll_pages(self, soup, html, page1_url):
        base_url = '/'.join(page1_url.split('/')[:-1]) + '/%s.html'

        returns = []
        soup = BeautifulSoup(html)
        img_urls = soup.find('div', id='viewer').find_all('img')
        # LOG.info(img_urls)
        for img_url in img_urls:
            returns.append(img_url.attrs['data-original'])
        return returns

    def _chapter_pages(self, soup, html, page1_url):
        base_url = '/'.join(page1_url.split('/')[:-1]) + '/%s.html'

        # a <select> tag has options that each points to a page
        opts = soup.find('select', class_='mangaread-page').find_all('option')
        urls = [opt['value'] for opt in opts]

        # Page 1 has already been fetched (stored in this html param, duh!)
        # so let's save ourselves an http request
        pages_htmls = []
        session = FuturesSession()

        for order, url in enumerate(urls):
            res = session.get(url).result()
            if res.status_code != 200:
                raise HtmlError('cannot fetch')
            pages_htmls.append(res.content)

        returns = []
        for page_html in pages_htmls:
            soup = BeautifulSoup(page_html)
            img_url = soup.find('div', id='viewer').find('img').attrs['src']
            returns.append(img_url)
        return natsorted(returns)

    def _chapter_series_url(self, url):
        origin = url.replace('/roll_manga', '/manga')
        return origin.rsplit('/', 2)[0]

    def fetch_chapter_seed_page(self, url):
        try:
            return (self.get_html(self._normalize_chapter_href(url)),
                    self._normalize_chapter_href(url))
        except HtmlError:
            return (self.get_html(url.replace('/roll_manga', '/manga')),
                    url.replace('/roll_manga', '/manga'))

    def _series_list(self, url, params=None, type=None):

        resp = requests.get(url, params)
        search_results = {}
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.content)
        list_manga = soup.find('ul', class_='manga-list')

        if list_manga is None:  # no author of this name
            return []
        list_li = list_manga.find_all('li')
        # print(list_li)
        for order, li in enumerate(list_li):
            series_link = li.find('a').attrs['href']
            chapter_link = li.find('a', class_='ch-button').attrs['href']
            chapter_text = li.find('a', class_='ch-button').text
            cover_src = li.find('img').attrs['src']
            info = li.find('div', class_='cover-info').find_all('p')

            search_results[order] = dict(name=info[0].text,
                                         genres=info[1].text,
                                         manga_url=series_link,
                                         last_chapter=chapter_link,
                                         last_ch_name=chapter_text,
                                         thumb_url=cover_src)
            if type in ['search', 'hot']:
                search_results[order].update({"author": info[2].text,
                                              "rank": info[3].text.replace('Rank:', '')})
            elif type in 'latest':
                search_results[order].update({
                    "status": info[2].text.replace('Status:', ''),
                    "last_date": info[3].text})

        """
             {
                "name": "Akatsuki No Yona",
                "genres": "Shoujo, Action",
                "no": "85",
                "cover": "http://a.mhcdn.net/store/manga/9456/thumb_cover.jpg?v=1430789336",
                "last_chapter": "http://m.mangahere.co/manga/akatsuki_no_yona/c085/",
                "manga_url": "http://m.mangahere.co/manga/akatsuki_no_yona/",
                "author": "KUSANAGI Mizuho",
                "rank": "41th"
            }
        """
        # print(search_results)
        # Get ordered list of series results
        series = []
        for i in sorted(search_results):
            series.append(search_results[i])
        return series

