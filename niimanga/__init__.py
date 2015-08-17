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
 #  __init__.py.py
"""

import os
from pyramid.config import Configurator as Conf
import niimanga.libs.security
import niimanga.routes
import niimanga.configs.session
import niimanga.configs.path
import niimanga.configs.cors
import niimanga.models
import niimanga.configs.view


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    here = os.path.dirname(__file__)
    # set directory mako templates
    settings['mako.directories'] = '{egg}:templates'.format(egg=__name__)
    settings['storage.base_path'] = "".join([here, settings['storage.base_path']])

    # settings['storage.base_url'] = 'store/manga/'
    # settings['storage.extensions'] = 'images+archives'

    cfg = Conf(settings=settings)

    # set root package
    cfg.registry.pack = __name__

    cfg.registry.here = here
    # cfg.set_request_factory(RequestWithUserAttribute)
    # set security policy auth dan authz
    cfg.include(niimanga.libs.security)

    # set session implement factory
    # cfg.set_session_factory()

    # set path folder manga
    cfg.include(niimanga.configs.path)

    # set Route DInjection
    cfg.include(niimanga.routes)

    # set Database Session DInjection
    cfg.include(niimanga.configs.session)

    # set Database Configuration
    cfg.include(niimanga.models)

    # set cors Configuration
    # cfg.include(niimanga.configs.cors)

    # set asset static Configuration
    cfg.include(niimanga.configs.view)

    return cfg.make_wsgi_app()