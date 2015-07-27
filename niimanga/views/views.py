"""
 # Copyright (c) 02 2015 | surya
 # 21/02/15 nanang.ask@kubuskotak.com
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
 #  views.py
"""
from Queue import Queue
import logging
from threading import Thread

from niimanga import sites
from niimanga.libs.exceptions import HtmlError
from niimanga.libs.ziputils import print_info, extract_zip
from pyramid.response import FileResponse
from pyramid.view import view_config
from pyramid_debugtoolbar.panels import traceback


LOG = logging.getLogger(__name__)


# @view_config(route_name='home', renderer='mytemplate.html')
# def my_view(request):
#     return {'project': 'moori'}

@view_config(route_name='upload',
             request_method='POST', renderer='json')
def upload(request):
    # print(request.POST)
    # simpan di temps/uuid/chapter-id/
    post = request.POST
    f = post['DROPZONE']
    uuid = post['uuid']
    folders = 'temps'
    fupload = '/'.join([folders, uuid])

    if not request.storage.exists(fupload):
        request.storage.save(f, folder=fupload)
        filezip = request.storage.path('/'.join([fupload, f.filename]))

        # print_info(filezip)
        # extract_zip(filezip,  request.storage.path(fupload))
        LOG.debug('okey')
    LOG.debug(request.storage.url(fupload))
    # return HTTPSeeOther(request.route_url('home'))
    return dict(status=200)


@view_config(route_name='download')
def download(request):

    filename = request.params['filename']
    path = request.storage.path(filename)
    url = request.storage.url(filename)
    print(url)
    return FileResponse(path)


@view_config(route_name='search_manga', renderer='json',
             request_method='GET')
def search_manga(request):
    keyword = request.params.get('keyword')
    type = request.params.get('type')
    search_results = {}

    if type == 'name':
        func_name = 'search_series'
    elif type == 'author':
        func_name = 'search_by_author'
    elif type == 'latest':
        func_name = 'search_latest'
    elif type == 'hot':
        func_name = 'search_hot'
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


@view_config(route_name='manga', renderer='json')
def manga_home(request):
    url = request.params.get('url')
    # Check if this url is supported
    site = sites.get_site(url)
    series_page = site.fetch_manga_seed_page(url)
    series = site.series_info(series_page)

    return series


@view_config(route_name='chapter_manga', renderer='json')
def chapter_manga(request):

    url = request.params.get('url')
    series_url = request.params.get('site')
    # Check if this url is supported
    site = sites.get_site(url)
    chapter_page, url = site.fetch_chapter_seed_page(url)

    chapter = site.chapter_info(chapter_page, url=url)
    chapter.update({'site': series_url})

    return chapter



