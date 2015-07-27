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
 #  manga.py
"""
from Queue import Queue
from threading import Thread

from niimanga import sites
from niimanga.configs.view import ZHandler
from niimanga.libs.exceptions import HtmlError
from niimanga.models.mongo import insert_or_update_manga, db, in_or_up_manga_home, in_or_up_chapters
from pyramid.view import view_config
from pyramid_debugtoolbar.panels import traceback


class MangaView(ZHandler):
    @view_config(route_name="search_all", renderer="manga/hot.html")
    def search_view(self):
        _ = self.R
        keyword = _.params.get('keyword')
        type = _.params.get('type')
        mangas = self._search_manga(type=type, keyword=keyword)
        obj = insert_or_update_manga(mangas)
        return dict(project="apps", mangas=obj, caption='SEARCH')

    @view_config(route_name="manga_genre", renderer="manga/hot.html")
    def genre_view(self):
        _ = self.R
        genre = _.matchdict.get('genre')
        mangas = self._search_manga(type='genre', keyword=genre)
        obj = insert_or_update_manga(mangas)
        return dict(project="apps", mangas=obj, caption=genre)

    @view_config(route_name="list_genre", renderer="manga/list_genres.html")
    def genre_list(self):
        _ = self.R
        genres = self._search_manga(type='list-genre')
        return dict(project="apps", genres=genres)

    @view_config(route_name="manga_home", renderer="manga/latest.html")
    def latest_view(self):
        request = self.R
        # mangas = Manga.query.order_by(Manga.created_at.desc()).all()
        # mangas = Manga.recent()

        # for manga in mangas:
        #     for genre in manga.genres:
        #         print(genre)
        #     for author in manga.authors:
        #         print(author)

        # mangas = Manga.recent()
        mangas = self._search_manga(type='latest')
        obj = insert_or_update_manga(mangas)

        return dict(project="apps", mangas=obj)

    @view_config(route_name="manga_hot", renderer="manga/hot.html")
    def hot_view(self):
        mangas = self._search_manga(type='hot')
        obj = insert_or_update_manga(mangas)
        return dict(project="apps", mangas=obj, caption='HOT')

    # @view_config(route_name="manga_title", renderer="manga/home.html")
    def manga_home(self):
        request = self.R

        title = request.matchdict.get('title_slug', None)
        # cari manga by slug
        mangadb = db.manga.find_one({'slug': title})
        site = sites.get_site(mangadb.get('manga_url'))
        series_page = site.fetch_manga_seed_page(mangadb.get('manga_url'))
        series = site.series_info(series_page)
        manga = in_or_up_manga_home(mangadb.get('manga_url'), series)
        chapters = in_or_up_chapters(series.get('chapters', []), title, mangadb.get('manga_url'))
        return dict(project="app", manga=manga, chapters=chapters)

    def _search_manga(self, type, keyword=u''):
        search_results = {}

        if type == 'name':
            func_name = 'search_series'
        elif type == 'author':
            func_name = 'search_by_author'
        elif type == 'latest':
            func_name = 'search_latest'
        elif type == 'hot':
            func_name = 'search_hot'
        elif type == 'genre':
            func_name = 'search_genre'
        elif type == 'list-genre':
            func_name = 'list_genre'
        else:
            raise HtmlError('invalid_type')

        def _search(queue):
            keyword, site, order = queue.get()
            search_func = getattr(site, func_name)
            try:
                series_list = search_func(str(keyword))
                search_results[order] = series_list
            except Exception as ex:
                print(traceback.escape(ex.message))
                search_results[order] = []
            queue.task_done()

        q = Queue()

        for order, site in enumerate(sites.available_sites):
            q.put((keyword, site, order))
            worker = Thread(target=_search, args=(q,))
            worker.setDaemon(True)
            worker.start()

        q.join()
        # print(search_results)
        # Get ordered list of series results
        series = []
        for i in sorted(search_results):
            series.extend(search_results[i])
        return series