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