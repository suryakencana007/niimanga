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
 #  session.py
"""
from pyramid.decorator import reify
from niimanga.models import DBSession
from sqlalchemy import engine_from_config


def includeme(config):
    settings = config.registry.settings
    # Store DB connection in registry
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    config.registry.engine = engine

    @reify
    def _get_db(request):

        session = DBSession
        session.configure(bind=engine)
        # session = Session()

        def cleanup(request):
            # if request.exception is not None:
            #     session.rollback()
            # else:
            #     session.commit()
            session.close()
            session.remove()
        request.add_finished_callback(cleanup)
        return session
    config.add_request_method(_get_db, 'db')