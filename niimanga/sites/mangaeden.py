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
 #  mangaeden.py
"""
import urllib

from bs4 import BeautifulSoup
import bs4
from niimanga.libs.exceptions import HtmlError
from niimanga.sites import Site
import requests
from requests_futures.sessions import FuturesSession


class MangaEden(Site):

    netlocs = [
        'www.mangaeden.com',
        'mangaeden',
        'http://www.mangaeden.com',
        'http://cdn.mangaeden.com/mangasimg/200x/',
        'ed'
    ]

    def search_latest(self, keyword=None):
        url = self.netlocs[2] + '/ajax/news/1/0/1/'
        resp = requests.get(url)

        search_results = []
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.content)

        try:
            # table = soup.find('table', class_='chapters_list')
            en_rows = soup.find_all('li', class_='topMangaHome')
            # print(len(en_rows))
            # print(soup.find_all('li', {'class': 'hotTopMangaHome'}))
            for i, rows in enumerate(en_rows):
                # print(rows['class'])
                if 'hotTopMangaHome' not in rows['class']:
                    div_thumb = rows.find('div', class_='hottestImage')
                    image_thumb = div_thumb.find('img').attrs['data-src']

                    div_info = rows.find('div', class_='hottestInfo')

                    origin_url = div_info.find('a', class_='mangaUrl').attrs['href']
                    title = div_info.find('a', class_='mangaUrl').text

                    last_title = div_info.find('span', class_='chapterBox')
                    if last_title is None:
                        last_title = div_info.find('a', class_='chapterLink').text
                        last_url = div_info.find('a', class_='chapterLink').attrs['href']
                    else:
                        last_title = last_title.text
                        last_url = div_info.find('a', class_='flagContainer').attrs['href']

                    # print(last_title)

                    time = div_info.find('div', class_='chapterDate').text
                    search_results.append(
                        dict(
                            thumb=self.netlocs[3] + "/".join([image_thumb.split('/')[-2], image_thumb.split('/')[-1]]),
                            origin=origin_url,
                            name=title,
                            # time=self.parseDate.human_to_date_stamp(time),
                            time=time,
                            last_chapter=last_title,
                            last_url=last_url,
                            site=self.netlocs[1]
                        )
                    )
            return search_results
        except AttributeError as e:
            print(e.message)
            return []

    def search_by_author(self, author):
        url = self.netlocs[2] + '/en-directory/?author=' + urllib.quote(author)
        resp = requests.get(url)

        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.content)

        try:
            table = soup.find('table', id='mangaList')
            rows = table.find_all('tr', class_='')
            hrefs = [tr.find('td').find('a')
                     for tr in rows if 'style' not in tr.attrs]

            return [
                {
                    'name': a.text.strip(),
                    'url': a['href'],
                    'site': self.netlocs[1]
                } for a in hrefs
            ]

        except Exception:
            return []

    def _chapters(self, soup):
        try:
            table = soup.find('tbody')
            rows = table.find_all('tr')

            chapters = []
            for row in rows:
                a = row.find('a')
                url = a['href']
                name = a.find('b').text.strip()
                time = row.find_all('td')[-1].text.strip()
                print(time)
                chapters.append({
                    'name': name,
                    'url': url,
                    'time': time
                })
            return chapters

        except AttributeError:
            return []

    def _thumbnail_url_and_tags(self, soup):
        try:
            box = soup.find('div', id='rightContent')
            thumb = box.find('div', class_='mangaImage2').find('img')['src']

            # This cell stores <a> that store tags
            tags_siblings = box.find('h4', text='Genres').next_siblings
            tags = []
            for s in tags_siblings:
                if type(s) == bs4.element.Tag and s.name == 'a':
                    tags.append(s.text.strip().lower())

            return thumb, tags
        except AttributeError:
            return [], []

    def _name(self, soup):
        return soup.find('h2', class_='enIcon').contents[0].strip()

    def _alias(self, soup):
        box = soup.find('div', id='rightContent')
        siblings = box.find('h4', text='Alternative name(s)').next_siblings
        result = []
        for s in siblings:
            if s.name == 'h4':
                break
            if type(s) == bs4.element.NavigableString:
                result.append(s.strip().lower())
        return result

    def _status(self, soup):
        box = soup.find('div', id='rightContent')
        siblings = box.find('h4', text='Status').next_siblings
        for s in siblings:
            if type(s) == bs4.element.NavigableString:
                return s.strip().lower()
        return 'unknown'

    def _authors(self, soup):
        box = soup.find('div', id='rightContent')
        authors = box.find('h4', text='Author').next_siblings
        results = []
        for s in authors:
            if type(s) == bs4.element.Tag and s.name == 'a':
                name = s.text.strip().lower()
                if name not in results:
                    results.append(name)
            if s.name == 'br':
                break
        return results

    def _artists(self, soup):
        box = soup.find('div', id='rightContent')
        artists = box.find('h4', text='Artist').next_siblings
        results = []
        for s in artists:
            if type(s) == bs4.element.Tag and s.name == 'a':
                name = s.text.strip().lower()
                if name not in results:
                    results.append(name)
            if s.name == 'br':
                break
        return results

    def _description(self, soup):
        return soup.find('p', id='mangaDescription').get_text()

    def series_info(self, html):
        soup = BeautifulSoup(html)
        chapters = self._chapters(soup)
        thumb_url, tags = self._thumbnail_url_and_tags(soup)
        name = self._name(soup)
        aka = self._alias(soup)
        status = self._status(soup)
        description = self._description(soup)
        authors = self._authors(soup)
        artists = self._artists(soup)

        return {
            'chapters': chapters,
            'thumb_url': thumb_url,
            'name': name,
            'aka': aka,
            'tags': tags,
            'status': status,
            'description': description,
            'authors': authors,
            'artists': artists,
            'site': self.netlocs[1]
        }

    def chapter_info(self, html, **kwargs):
        soup = BeautifulSoup(html)
        pages = self._chapter_pages(soup, html)
        name = self._chapter_name(soup)
        series_url = self._chapter_series_url(soup)
        prev, next = self._chapter_prev_next(soup)
        return {
            'name': name,
            'pages': pages,
            'series_url': series_url,
            'next_chapter_url': next,
            'prev_chapter_url': prev,
            }

    def _chapter_pages(self, soup, html):

        # a <select> tag has options that each points to a page
        neighbour = soup.find('select', id='combobox').find_next_sibling('select')
        opts = neighbour.find_all('option')
        urls = [opt['value'] for opt in opts]

        # Page 1 has already been fetched (stored in this html param, duh!)
        # so let's save ourselves an http request
        pages_htmls = [html]
        urls = urls[1:]
        session = FuturesSession()

        for order, url in enumerate(urls):
            uri = self.netlocs[2] + url
            print(uri)
            res = session.get(uri).result()
            if res.status_code != 200:
                raise HtmlError('cannot fetch')
            pages_htmls.append(res.content)

        returns = []
        for page_html in pages_htmls:
            soup = BeautifulSoup(page_html)
            img_url = soup.find('img', id='mainImg')['src']
            returns.append(img_url)
        return returns

    def _chapter_name(self, soup):
        select = soup.find('select', id='combobox')
        return select.find('option', selected=True)['value']

    def _chapter_series_url(self, soup):
        a_tag = soup.find('div', class_='top-title').find_all('a')
        return a_tag[2]['href']

    def _chapter_prev_next(self, soup):
        url = self._chapter_series_url(soup)
        select = soup.find('select', id='combobox')
        opts = select.find('option', selected=True)

        next = opts.find_next_siblings('option')
        if next is not None:
            next = url + next[0]['value']
        prev = opts.find_previous_siblings('option')
        if len(prev) > 0:
            prev = url + prev[0]['value']
        return prev, next