"""
 # Copyright (c) 03 2015 | surya
 # 02/03/15 nanang.ask@kubuskotak.com
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
from Queue import Queue
import logging
from threading import Thread
from datetime import datetime, timedelta
import arrow
from dateutil import tz

from niimanga import sites
from niimanga.libs.manga import MangaUtil
from niimanga.libs.ziputils import extract_zip
from niimanga.models.manga import Chapter, Manga
from niimanga.models.master import Genre
from pyramid.view import view_config
from niimanga.libs.access import api_auth
from niimanga.libs.oauth.authorization import client_credentials_authorization
from niimanga.libs.oauth.request import RequestOAuth
from niimanga.libs.utils import ResponseHTTP, LocalDateTime, slugist
from niimanga.models.auth import UserMgr
from niimanga.configs.view import ZHandler
from sqlalchemy import desc, and_


LOG = logging.getLogger(__name__)


class ApiView(ZHandler):
    @view_config(route_name="api_ping", renderer="json")
    @api_auth('api_key', UserMgr.get)
    def ping(self):
        """Verify that you've setup your api correctly and verified

        """
        with ResponseHTTP(response=self.R.response) as t:
            i = [i for i in range(5000)]
            code, status = ResponseHTTP.INTERNAL_SERVER_ERROR
        return t.to_json(u'success', code=code, status=status, data={'ok': 'jamur'})

    @view_config(route_name="token_endpoint", renderer="json")
    def get_token(self):
        """Get Token dengan Api-key authz
            :GET ?grant_type=client_credentials&scope=member:basic
            Set Header
            :param Authorization i.e basic client_key:client_secret
            :param grant_type i.e [client_credentials, password, authorization_code]
        """
        request = RequestOAuth(self.R)

        with ResponseHTTP(request.response) as resp:
            grant_type = request.params.get('grant_type', None)
            _in = u'Failed'
            code, status = ResponseHTTP.NOT_AUTHORIZED
            message = 'authentication'
            if u'client_credentials' in grant_type:
                # optional scope
                scope = request.params.get('scope', 'member:basic')
                if scope:
                    scope = scope.split(' ')
                if request.authentication is not None:
                    LOG.debug('authentication')
                    return client_credentials_authorization(request.authentication, scope)
                LOG.debug('client_credentials')

            if u'authorization_code' in grant_type:
                code, status = ResponseHTTP.NOT_AUTHORIZED

            if u'password' in grant_type:
                code, status = ResponseHTTP.NOT_AUTHORIZED

        return resp.to_json(_in,
                            message=message,
                            code=code,
                            status=status)


class MangaApi(ZHandler):

    @staticmethod
    def _card_fill(_, cards):
        lt = arrow.utcnow()
        results = []
        for row in cards:
            past = arrow.get(row.chapter_updated.replace(tzinfo=tz.tzlocal()))
            time = past.humanize(lt)
            filename = '/'.join([row.id, row.thumb])
            thumb = _.storage.url(filename)
            chapter = row.last_chapter(row.id)
            # chapter = Chapter.query.first()
            card = dict(
                thumb=thumb,
                origin='/'.join([row.slug]),
                name=row.title,
                time=time,
                last_chapter=' '.join(['Ch.', str(chapter.chapter).replace('.0', ''), chapter.title]),
                last_url='/'.join([row.slug, chapter.slug]),
                site='batoto' if 'bt' in row.type else 'mangaeden' if 'ed' in row.type else 'kk'
            )
            results.append(card)
        return results

    @view_config(route_name='latest_manga', renderer='json', request_method='POST')
    def latest_manga(self):
        _ = self.R
        limit = int(_.params.get('cards', 16))
        offset = int(_.params.get('page', 1)) * limit
        """ output
            dict(
            url = request.storage.url(filename)
                thumb=self.netlocs[3] + "/".join([image_thumb.split('/')[-2], image_thumb.split('/')[-1]]),
                origin=origin_url,
                name=title,
                # time=self.parseDate.human_to_date_stamp(time),
                time=time,
                last_chapter=last_title,
                last_url=last_url,
                site=self.netlocs[1]
            )
        """
        qry = Manga.query
        latest = qry \
            .filter(Manga.chapter_count > 0) \
            .order_by(desc(Manga.chapter_updated)) \
            .offset(offset) \
            .limit(limit) \
            .all()
        return MangaApi._card_fill(_, latest)

    @view_config(route_name='popular_manga', renderer='json')
    def popular_series(self):
        _ = self.R
        limit = int(_.params.get('cards', 5))
        offset = int(_.params.get('page', 1)) * limit
        qry = Manga.query
        popular = qry.filter(Manga.chapter_count > 0) \
            .order_by(desc(Manga.viewed)) \
            .offset(offset) \
            .limit(limit) \
            .all()
        return MangaApi._card_fill(_, popular)

    @view_config(route_name="series_manga", renderer='json', request_method='POST')
    def series_page(self):
        _ = self.R
        slug = _.matchdict.get('series_slug', "No Title")
        present = arrow.utcnow()
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
            status = manga.status
            stags = manga.get_genre_tostr()
            tags = [dict(label=tag, value=slugist(tag))for tag in stags.split(',')]
            time = arrow.get(manga.chapter_updated.replace(tzinfo=tz.tzlocal())).humanize(present)
            origin = manga.origin
            last = Manga.last_chapter(manga.id)
            last_chapter = ' '.join([str(last.chapter), last.title])
            last_url = '/'.join([manga.slug, last.slug])

            manga.updated_viewed()

            results = []
            chapters = Chapter.query.filter_by(tb_manga_id=manga.id).order_by(desc(Chapter.sortorder)).all()
            for chapter in chapters:
                results.append(dict(
                    name=' '.join(['Ch.', str(chapter.chapter).replace('.0', ''), chapter.title]),
                    url='/'.join([manga.slug, chapter.slug]),
                    time=arrow.get(chapter.updated.replace(tzinfo=tz.tzlocal())).humanize(present)
                ))

            return dict(
                origin=origin,
                aka=aka,
                thumb_url=thumb,
                artists=artists,
                authors=authors,
                description=description,
                name=name,
                tags=tags,
                status=status,
                time=time,
                last_chapter=last_chapter,
                last_url=last_url,
                chapters=results
            )
        return None

    @view_config(route_name='chapter_manga', renderer='json', request_method='POST')
    def chapter_view(self):
        """
            pages: [],
                name: '',
                series_name: '',
                next_chapter_url: null,
                prev_chapter_url: null
        :return:
        """
        _ = self.R
        slug = _.matchdict.get('series_slug', "No Title")
        chap_slug = _.matchdict.get('chapter_slug', "No Title")

        # cari manga by slug
        manga = Manga.query.filter(Manga.slug == slug).first()
        manga.updated_viewed()
        LOG.debug(manga.slug)
        # cari chapter manga
        chapter = manga.get_chapter(manga, chap_slug)

        path = _.storage.base_path

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
            urlmanga = _.static_url('niimanga:rak/manga/{manga_id}/{chapter_id}/{file}'
                                    .format(manga_id=manga.id,
                                            chapter_id=chapter.id,
                                            file=manga_list.get_item_by_key(item)[1]))
            page_img.append(urlmanga)

        return dict(
            pages=page_img,
            name=' '.join(['Ch.', str(chapter.chapter).replace('.0', ''), chapter.title]),
            series_url=manga.slug,
            next_chapter_url=None,
            prev_chapter_url=None
        )

    @view_config(route_name='search_series', renderer='json')
    def search_series(self):
        _ = self.R
        q = _.params.get('q', '')
        qry = Manga.query
        results = qry.filter(and_(Manga.title.ilike('%{q}%'.format(q=q)), Manga.chapter_count > 0)) \
            .order_by(desc(Manga.chapter_updated)) \
            .all()
        if results:
            return MangaApi._card_fill(_, results)
        return dict({error: 'there is error from Manga Record Collections'})

    @view_config(route_name='upload_chapter',
                 request_method='POST', renderer='json')
    def upload_chapter(self):
        _ = self.R
        # simpan di temps/uuid/
        post = _.POST
        uuid, f = post['uuid'], post['DROPZONE']
        fupload = '/'.join(['temps', uuid])

        if not _.storage.exists(fupload):
            _.storage.save(f, folder=fupload)
            # filezip = _.storage.path('/'.join([fupload, f.filename]))
            # extract_zip(filezip,  _.storage.path(fupload))
            LOG.debug('okey')
        LOG.debug(_.storage.url(fupload))
        # return HTTPSeeOther(request.route_url('home'))
        return dict(status=200)

    @view_config(route_name='list_genres', renderer='json')
    def list_genre(self):
        _ = self.R
        rows = []
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            q = _.params.get('q', None)
            if q is not None:
                genres = Genre.query.filter(Genre.name.ilike('%{0}%'.format(q))).all()
                for gen in genres:
                    rows.append(dict(
                        label=str(gen.name).capitalize(),
                        value=gen.slug
                    ))
                _in = u'Success'
                code, status = ResponseHTTP.OK
        return resp.to_json(_in,
                            code=code,
                            status=status, rows=rows)

    @view_config(route_name='search_genre', renderer='json')
    def search_genre(self):
        _ = self.R
        q = _.params.get('q', '')
        qry = Manga.query
        results = qry.filter(Manga.chapter_count > 0) \
            .join(Manga.genres).filter(Genre.slug == q) \
            .all()
        return MangaApi._card_fill(_, results)