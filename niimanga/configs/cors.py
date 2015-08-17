"""
 # Copyright (c) 08 2015 | surya
 # 15/08/15 nanang.ask@kubuskotak.com
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
 #  cors.py
"""
from pyramid.request import Request
from pyramid.response import Response


def includeme(config):

    def _req_factory(environ):
        R = Request(environ)
        if R.is_xhr:
            R.response = Response()
            R.response.headerlist = []
            R.response.headerlist.extend(
                (
                    ('Access-Control-Allow-Origin', '*'),
                    ('Content-Type', 'application/json')
                )
            )
        return R
    config.set_request_factory(_req_factory)