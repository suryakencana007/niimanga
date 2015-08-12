"""
 # Copyright (c) 04 2015 | surya
 # 21/04/15 nanang.ask@kubuskotak.com
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
 #  main.py
"""

from niimanga.configs.view import ZHandler
from niimanga.libs.crawlable import CrawlAble
from niimanga.models.manga import Manga
from pyramid.view import view_config


class MainView(ZHandler):

    @view_config(route_name='home', renderer='layouts/home.html')
    @CrawlAble()
    def home_view(self):

        return {'project': 'moori'}

    @view_config(route_name='url_popular', renderer='layouts/home.html')
    @CrawlAble()
    def popular_view(self):

        return {'project': 'moori'}

    @view_config(route_name='url_latest', renderer='layouts/home.html')
    @CrawlAble()
    def latest_view(self):

        return {'project': 'moori'}

    @view_config(route_name='url_series', renderer='layouts/series.html')
    @CrawlAble()
    def series_view(self):
        _ = self.R
        slug = _.matchdict.get('seriesSlug', "No Title")
        print(slug)
        qry = Manga.query
        manga = qry.filter(Manga.slug == slug.strip()).first()
        if manga is not None:
            filename = '/'.join([manga.id, manga.thumb])
            thumb = _.storage.url(filename)
            aka = manga.aka
            artists = manga.get_artist()
            authors = manga.get_authors()
            description = manga.description
            name = manga.title
            last = Manga.last_chapter(manga.id)
            last_chapter = ' '.join([str(last.chapter), last.title])

            return dict(
                aka=aka,
                url='/manga/{slug}'.format(slug=slug),
                thumb_url=thumb,
                artists=artists,
                authors=authors,
                description=description,
                name=name,
                last_chapter=last_chapter
            )
        return {'project': 'moori'}

    @view_config(route_name='url_chapter', renderer='layouts/chapter.html')
    @CrawlAble()
    def chapter_view(self):
        _ = self.R
        slug = _.matchdict.get('seriesSlug', "No Title")
        chap_slug = _.matchdict.get('chapterSlug', "No Title")

        # cari manga by slug
        manga = Manga.query.filter(Manga.slug == slug).first()
        if manga is not None:
            filename = '/'.join([manga.id, manga.thumb])
            thumb = _.storage.url(filename)
            aka = manga.aka
            artists = manga.get_artist()
            authors = manga.get_authors()
            description = manga.description
            name = manga.title
            last = Manga.last_chapter(manga.id)
            last_chapter = ' '.join([str(last.chapter), last.title])
            # cari chapter manga
            chapter = manga.get_chapter(manga, chap_slug)
            return dict(
                aka=aka,
                url='/chapter/{slug}/{chap}'.format(slug=slug, chap=chap_slug),
                thumb_url=thumb,
                artists=artists,
                authors=authors,
                description=description,
                name=' '.join([name, '|', 'Ch.', str(chapter.chapter).replace('.0', ''), chapter.title]),
                last_chapter=last_chapter
            )
        return {'project': 'moori'}

    @view_config(route_name='url_search', renderer='layouts/home.html')
    @CrawlAble()
    def search_view(self):

        return {'project': 'moori'}

    @view_config(route_name='url_genre', renderer='layouts/home.html')
    @CrawlAble()
    def genre_view(self):

        return {'project': 'moori'}

    @view_config(context='pyramid.exceptions.NotFound', renderer='layouts/404.html')
    def not_found_view(self):
        return {'project': 'moori'}