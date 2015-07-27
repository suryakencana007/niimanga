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
 #  view.py
"""


def includeme(config):
    settings = config.registry.settings

    # Templates ending in ".html" should be rendered with Mako.
    config.add_mako_renderer(".html")

    # set view Configuration
    config.add_static_view(name=settings['static_assets'],
                           path='{egg}:public'.format(egg=config.registry.pack),
                           cache_max_age=3600)
    config.add_static_view(name=settings['static_manga'],
                           path='{egg}:rak/manga'.format(egg=config.registry.pack),
                           cache_max_age=3600)
    config.add_static_view(name=settings['static_common'],
                           path='{egg}:rak/common'.format(egg=config.registry.pack),
                           cache_max_age=3600)

    config.scan('{egg}.views'.format(egg=config.registry.pack))


class ZHandler(object):
    def __init__(self, request):
        self.R = request