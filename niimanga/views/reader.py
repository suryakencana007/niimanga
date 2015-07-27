"""
 # Copyright (c) 04 2015 | surya
 # 20/04/15 nanang.ask@kubuskotak.com
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
 #  reader.py
"""
import logging
from niimanga import sites

from niimanga.configs.view import ZHandler
from niimanga.libs.manga import MangaUtil, parse_chapter
from niimanga.models.manga import Manga
from niimanga.models.mongo import db, in_or_up_chapters, in_or_up_manga_home
from pyramid.view import view_config


LOG = logging.getLogger(__name__)


class ReaderManga(ZHandler):

    @view_config(route_name="moco_manga", renderer="json")
    def moco_manga(self):

        request = self.R
        title = request.matchdict.get('title_slug', "No Title")
        chapter_slug = request.matchdict.get('chapter_no', "ch.0")

        # cari manga by slug
        manga = Manga.query.filter(Manga.slug == title).first()
        manga.updated_viewed()
        LOG.debug(manga.slug)
        # cari chapter manga
        chapter = manga.get_chapter(manga, chapter_slug)

        path = request.storage.base_path

        manga_list = MangaUtil(path, manga.id, chapter.id)

        manga_list.build_image_lookup_dict()
        # for key in manga.items:
        #     print(key)
        """
            /store/{manga_id}/{chapter_id/filenames
            untuk folder manga storage digunakan gendID manga e.g /store/2589637412/897589647/filenames
        """

        page_img = []
        for item in manga_list.items:
            LOG.debug(manga_list.get_item_by_key(item)[1])
            urlmanga = request.static_url('niimanga:rak/manga/{manga_id}/{chapter_id}/{file}'
                                          .format(manga_id=manga.id,
                                                  chapter_id=chapter.id,
                                                  file=manga_list.get_item_by_key(item)[1]))
            page_img.append(urlmanga)

        # request.db.add(manga)
        return dict(ch=chapter_slug, chapters=page_img)

    # @view_config(route_name="moco_manga", renderer="manga/reader/moco.html")
    def moco_manga_bak(self):

        request = self.R
        title = request.matchdict.get('title_slug', "No Title")
        chapter_slug = request.matchdict.get('chapter_no', "ch.0")
        chapter = db.chapter.find_one({'slug': chapter_slug})

        # manga ada chapter belum terrecord
        if chapter is None:
            mangadb = db.manga.find_one({'slug': title})
            site = sites.get_site(mangadb.get('manga_url'))
            series_page = site.fetch_manga_seed_page(mangadb.get('manga_url'))
            series = site.series_info(series_page)
            in_or_up_manga_home(mangadb.get('manga_url'), series)
            in_or_up_chapters(series.get('chapters', []), title, mangadb.get('manga_url'))

        chapter = db.chapter.find_one({'slug': chapter_slug})
        url = chapter.get('url')
        site = sites.get_site(url)
        chapter_page, url = site.fetch_chapter_seed_page(url)

        ch_page = site.chapter_info(chapter_page, url=url)

        return dict(home=title, chapter=chapter, pages=ch_page.get('pages', []))
