"""
 # Copyright (c) 03 2015 | surya
 # 11/03/15 nanang.ask@kubuskotak.com
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
from ConfigParser import SafeConfigParser
from logging.config import fileConfig
import unittest

import pkg_resources
from pyramid import testing
from niimanga.models import DBSession
from sqlalchemy import engine_from_config


def setup():
    """Setup the application given a config dictionary."""
    fname = pkg_resources.resource_filename("niimanga", "../development.ini")
    fileConfig(fname)
    config = SafeConfigParser()
    config.read(fname)
    settings = dict(config.items("app:main"))
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    return engine


class TestDBBase(unittest.TestCase):
    def setUp(self):
        super(TestDBBase, self).setUp()
        """Setup Tests"""

        self.connection = setup().connect()
        # self.trans = self.connection.begin()
        self.session = DBSession(bind=self.connection)

    def tearDown(self):
        """Tear down each test"""
        DBSession.remove()

        # self.trans.rollback()
        self.connection.close()
        self.session.close()
        super(TestDBBase, self).tearDown()


class TestViewBase(unittest.TestCase):
    def setUp(self):
        from pyramid.paster import get_app
        fname = pkg_resources.resource_filename("reportmob", "../development.ini")
        app = get_app(fname, 'main')
        from webtest import TestApp
        self.app = TestApp(app)

    def tearDown(self):
        """Tear down each test"""
        testing.tearDown()

    def _login_admin(self):
        """Make the login call to the app"""
        self.app.post(
            '/api/v1/login',
            params={
                "email": "nanang999.ask@gmail.com",
                "password": "asdf1234"
            },
            status=200)