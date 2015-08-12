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
 #  routes.py
"""
from niimanga.libs.utils import URI_API


def includeme(config):
    config.add_route('home', '/')
    config.add_route('hum', '/hum')
    config.add_route('logout', 'logout')
    config.add_route("reset", "{username}/reset/{reset_key}")
    config.add_route("search_all", "/search")

    config.add_route("search_manga", "/series")
    config.add_route("manga", "/manga", request_method='POST')
    # config.add_route("chapter_manga", "/chapter", request_method='POST')

    """
        API RestFull
    """
    """register API"""
    config.add_route('signup_process', '{URI}/signup'.format(URI=URI_API), request_method='POST')

    """"login untuk mendapatkan API Key"""
    config.add_route('login', '{URI}/login'.format(URI=URI_API), request_method='POST')

    """getToken untuk authorization fungsi API
    curl -u 84b56af69b59333957bbf927ee65be0560536513:Aa7M6n~BD.uMUFGtRqQB
    :GET /api/v1/token?grant_type=client_credentials&scope=member:basic
    :POST @tokenizer bearer :token
    """
    config.add_route('token_endpoint', '{URI}/token'.format(URI=URI_API), request_method='GET')

    # ping checks
    config.add_route('api_ping',
                     '/api/v1/{api_key}/ping',
                     request_method='GET')
    config.add_route('api_ping_missing_user',
                     '/api/v1/ping',
                     request_method='GET')
    config.add_route('api_ping_missing_api',
                     '/ping',
                     request_method='GET')

    config.add_route('api_header', '/ping/header', request_method='GET')
    config.add_route('upload', '/upload')
    config.add_route('download', '/download')
    """
        manga
    """
    #home page manga
    config.add_route('manga_home',
                     '/manga')
    #home page manga
    config.add_route('manga_hot',
                     '/manga/hot')
    #genre manga
    config.add_route('list_genre',
                     '/manga/genre')
    #genre manga
    config.add_route('manga_genre',
                     '/manga/genre/{genre}')
    # #page manga
    # config.add_route('manga_title',
    #                  '/manga/{title_slug}')
    # # slug-title, slug-chapter e.g /manga/fairy-tail/chapter-001
    config.add_route('moco_manga',
                     '/manga/{title_slug}/{chapter_no}')

    """
        api frontends manga
    """
    # search
    config.add_route('search_series', '{URI}/search'.format(URI=URI_API))
    # genre search
    config.add_route('search_genre', '{URI}/genre'.format(URI=URI_API))
    # latest
    config.add_route('latest_manga', '{URI}/latest'.format(URI=URI_API))
    # popular
    config.add_route('popular_manga', '{URI}/popular'.format(URI=URI_API))
    # series
    config.add_route('series_manga', '{URI}/series/{slug}'.format(URI=URI_API, slug='{series_slug}'))
    # chapter
    config.add_route('chapter_manga', '{URI}/chapter/{slug}/{chapter}'.format(URI=URI_API,
                                                                              slug='{series_slug}',
                                                                              chapter='{chapter_slug}'
                                                                              ))
    # upload file
    config.add_route('upload_chapter', '{URI}/upload'.format(URI=URI_API))
    # list genres
    config.add_route('list_genres', '{URI}/genres'.format(URI=URI_API))

    """
        cms
    """
    # cms main
    config.add_route('cms_main',
                     '/cms')
    # cms chapter
    config.add_route('cms_chapter',
                     '/cms/chapter/{action}')
    # cms series
    config.add_route('cms_series',
                     '/cms/series/{action}')
    # cms menu
    config.add_route('cms_menu',
                     '/cms/menu/{action}')
    # cms group
    config.add_route('cms_group',
                     '/cms/grp/{action}')
    # cms season
    config.add_route('cms_season',
                     '/cms/season/{action}')
    # cms slider image
    config.add_route('cms_slider',
                     '/cms/slider/{action}')

    # cms slider image detail
    config.add_route('cms_slider_detail',
                     '/cms/slimage/{action}')

    """
        route frontends
    """
    config.add_route('url_popular', '/popular')
    config.add_route('url_latest', '/latest')
    config.add_route('url_series', '/manga/{seriesSlug}')
    config.add_route('url_chapter', '/chapter/{seriesSlug}/{chapterSlug}')
    config.add_route('url_search', '/search/{q}')
    config.add_route('url_genre', '/genre/{q}')

