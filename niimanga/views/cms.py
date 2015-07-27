"""
 # Copyright (c) 05 2015 | surya
 # 05/05/15 nanang.ask@kubuskotak.com
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
 #  cms.py
"""
import logging
import shutil
from niimanga.libs.ziputils import extract_zip
from os import path, walk, makedirs

from niimanga.configs.view import ZHandler
from niimanga.libs import utils
from niimanga.libs.utils import FieldsGrid, ResponseHTTP, slugist
from niimanga.models.acl import Group
from niimanga.models.component import Menu, Slider, SliderImage
from niimanga.models.manga import Manga, Chapter
from niimanga.models.master import Season, ISOLang
from pyramid.view import view_config


LOG = logging.getLogger(__name__)


class CMSMain(ZHandler):
    @view_config(route_name='cms_main',
                 renderer="layouts/cms.html")
    def index(self):
        _ = self.R

        return dict(project="menu")


class ChapterView(ZHandler):
    @view_config(route_name='cms_chapter', match_param='action=search',
                 renderer='json')
    def search_chapter(self):
        _ = self.R
        rows = []
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            qry = Chapter.query
            q = _.params.get('q', None)
            if q is not None:
                data = qry.filter(Chapter.title.ilike('%{0}%'.format(q))).all()
                for row in data:
                    rows.append(dict(
                        label=row.title,
                        value=row.id
                    ))
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status, rows=rows)

    @view_config(route_name='cms_chapter', match_param='action=lang',
                 renderer='json')
    def iso_lang(self):
        _ = self.R
        rows = []
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            qry = ISOLang.query
            data = qry.all()
            if data is not None and len(data) > 0:
                for row in data:
                    rows.append(dict(
                        label=row.name,
                        value=row.iso
                    ))
                _in = u'Success'
                code, status = ResponseHTTP.OK
        return resp.to_json(_in,
                            code=code,
                            status=status, rows=rows)

    @view_config(route_name='cms_chapter', match_param='action=src',
                 renderer='json', request_method="POST")
    def dataset(self):
        _ = self.R
        qry = Chapter.query

        chapters = qry.all()
        return dict(
            total=qry.count(),
            rows=[
                dict(
                    id=chapter.id,
                    mangaid=chapter.manga.id,
                    manga=chapter.manga.title,
                    title=chapter.title,
                    volume=chapter.volume,
                    chapter=chapter.chapter,
                    lang=chapter.lang.iso,
                    slug=chapter.slug
                ) for chapter in chapters]
        )

    @view_config(route_name='cms_chapter', match_param='action=edit-able',
                 renderer='json', request_method='POST')
    def editable_save(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            qry = Chapter.query

            rdict = utils.loads(_.params.get("row", None))
            if rdict is not None and len(rdict) > 0:
                # manga = Manga.query.filter(Manga.id == rdict.get('mangaid', None)).first()
                # manga_title = "-".join([manga.type, manga.title])
                lang = ISOLang.query.filter(ISOLang.iso == rdict.get('lang', 'en')).first()
                chapter = qry.get(rdict.get('id', None))
                chapter.title = rdict.get('title', None)
                chapter.volume = rdict.get('volume', None)
                chapter.chapter = rdict.get('chapter', None)
                chapter.lang = lang

                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)

    @view_config(route_name='cms_chapter', match_param='action=save-new',
                 renderer='json', request_method='POST')
    def save_new(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            # for key, value in _.params.iteritems():
            #     print(":".join([key, value]))
            if _.params.get('title', None) is not None:
                manga = Manga.query.filter(Manga.id == _.params.get('series', None)).first()
                manga_slug = "-".join([manga.type, manga.title])
                lang = ISOLang.query.filter(ISOLang.iso == _.params.get('lang', 'en')).first()
                v = _.params.get('volume', 0)
                c = _.params.get('chapter', 0)

                chapter = Chapter(
                    _.params.get('title', None),
                    c if str(c).isdigit() else 0,
                    v if str(v).isdigit() else 0
                )
                slug_chapter = ' '.join([manga_slug, _.params.get('title', None)])

                manga.chapter_count += 1
                manga.updated_chapter()
                chapter.lang = lang
                chapter.updated = utils.datetime.now()
                chapter.manga = manga
                # s = 1000v + c
                # chapter.sortorder = (1000*float(v)) + float(c)
                chapter.sortorder = float(_.params.get('chapter', None))
                chapter.slug = slug_chapter
                _.db.add(chapter)
                chp_tmp = Chapter.query.filter(Chapter.slug == slugist(slug_chapter)).first()
                temps_path = _.storage.path('/'.join(['temps', _.params.get('uuid', None)]))
                print(temps_path)
                for root, dirs, files in walk(temps_path):
                    LOG.info(files)
                    for f in files:
                        fpath = '/'.join([temps_path, f])
                        fdest = _.storage.path('/'.join([manga.id, chp_tmp.id]))
                        print(fpath)
                        print(fdest)
                        extract_zip(fpath, fdest)
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)


class SeriesView(ZHandler):
    @view_config(route_name='cms_series', match_param='action=search',
                 renderer='json')
    def search_series(self):
        _ = self.R
        rows = []
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            qry = Manga.query
            q = _.params.get('q', None)
            if q is not None:
                data = qry.filter(Manga.title.ilike('%{0}%'.format(q))).all()
                for row in data:
                    rows.append(dict(
                        label=row.title,
                        value=row.id
                    ))
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status, rows=rows)

    @view_config(route_name='cms_series', match_param='action=src',
                 renderer='json', request_method="POST")
    def dataset(self):
        _ = self.R
        qry = Manga.query

        manga = qry.all()
        return dict(
            total=qry.count(),
            rows=[
                dict(
                    id=series.id,
                    title=series.title,
                    authors=series.get_authors(),
                    artist=series.get_artist(),
                    description=series.description,
                    category=series.category,
                    released=series.released,
                    status=series.status,
                    slug=series.slug
                ) for series in manga]
        )

    @view_config(route_name='cms_series', match_param='action=edit-able',
                 renderer='json', request_method='POST')
    def editable_save(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            qry = Manga.query

            rdict = utils.loads(_.params.get("row", None))
            if rdict is not None and len(rdict) > 0:
                series = qry.get(rdict.get('id', None))
                series.title = rdict.get('title', 'no title')
                series.set_authors(rdict.get('authors', ''))
                series.set_artist(rdict.get('artist', ''))
                series.description = rdict.get('description', '')
                series.category = rdict.get('category', 'ja')
                series.released = rdict.get('released', None)
                series.status = rdict.get('status', None)

                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)

    @view_config(route_name='cms_series', match_param='action=save-new',
                 renderer='json', request_method='POST')
    def save_new(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            # for key, value in _.params.iteritems():
            #     print(":".join([key, value]))
            if _.params.get('title', None) is not None:
                manga = Manga(
                    _.params.get('type', 'kk'),
                    _.params.get('title', None),
                    _.params.get('released', None),
                    _.params.get('genres', None),
                    _.params.get('authors', None),
                    _.params.get('artist', None),
                    _.params.get('aka', None),
                    _.params.get('description', None),
                    _.params.get('status', None)
                )
                manga.category = _.params.get('category', 'ja')
                _.db.add(manga)
                mng_tmp = Manga.query.filter(Manga.slug == slugist("-".join([_.params.get('type', 'kk'), _.params.get('title', None)]))).first()
                temps_path = _.storage.path('/'.join(['temps', _.params.get('uuid', None)]))

                for root, dirs, files in walk(temps_path):
                    LOG.info(files)
                    for f in files:
                        fpath = '/'.join([temps_path, f])
                        ext = str(f).split('.')[-1]
                        LOG.info(fpath)
                        fdest = _.storage.path('/'.join([mng_tmp.id]))
                        folder_zip = '/'.join([fdest, 'cover.{ext}'.format(ext=ext)])
                        if '.jpg' in folder_zip or '.png' in folder_zip:
                            # LOG.info(folder_zip)
                            if not path.exists(fdest):
                                makedirs(fdest)
                            shutil.copy(fpath, folder_zip)
                            mng_tmp.thumb = '.'.join(['cover', ext])
                shutil.rmtree(temps_path)
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)


class MenuView(ZHandler):
    @view_config(route_name='cms_menu', match_param='action=list',
                 renderer="cms/menu/index.html")
    def index(self):
        _ = self.R
        cols_name = dict(id="ID", label="Label Menu", name="Route Name", url="Route Url")

        data = dict(title="Master Menu")

        return dict(project="menu", cols=cols_name, data=data)

    @view_config(route_name='cms_menu', match_param='action=src',
                 renderer='json', request_method="POST")
    def dataset(self):
        _ = self.R
        qry = Menu.query

        menu = qry.all()

        return dict(
            total=qry.count(),
            rows=[dict(id=mn.id, label=mn.label, name=mn.name, url=mn.url) for mn in menu]
        )

    @view_config(route_name='cms_menu', match_param='action=edit-able',
                 renderer='json', request_method='POST')
    def editable_save(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Success'
            code, status = ResponseHTTP.OK
            qry = Menu.query

            rdict = utils.loads(_.params.get("row", None))

            menu = qry.get(rdict.get('id', None))
            menu.name = rdict.get('name', '')
            menu.slug = rdict.get('name', '')
            menu.label = rdict.get('label', '')
            menu.url = rdict.get('url', '')

        return resp.to_json(_in,
                            code=code,
                            status=status)

    @view_config(route_name='cms_menu', match_param='action=save-new',
                 renderer='json', request_method='POST')
    def save_new(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            if _.params.get('label', None) is not None:
                menu = Menu(
                    _.params.get('label', None),
                    _.params.get('name', None),
                    _.params.get('url', None))
                _.db.add(menu)
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)


class GroupView(ZHandler):
    @view_config(route_name='cms_group', match_param='action=list',
                 renderer="cms/group/index.html")
    def index(self):
        _ = self.R
        cols_name = dict(id="ID", name="Group Name", slug="Slug Name")

        data = dict(title="Master Groups")

        return dict(project="group", cols=cols_name, data=data)

    @view_config(route_name='cms_group', match_param='action=src',
                 renderer='json', request_method="POST")
    def dataset(self):
        _ = self.R

        qry = Group.query

        group = qry.all()
        for grp in group:
            print(grp.id)

        return dict(
            total=qry.count(),
            rows=[dict(id=grp.id, name=grp.name, slug=grp.slug) for grp in group]
        )

    @view_config(route_name='cms_group', match_param='action=edit-able',
                 renderer='json', request_method='POST')
    def editable_save(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Success'
            code, status = ResponseHTTP.OK
            qry = Group.query

            rdict = utils.loads(_.params.get("row", None))

            group = qry.get(rdict.get('id', None))
            group.name = rdict.get('name', '')
            group.slug = rdict.get('name', '')

        return resp.to_json(_in,
                            code=code,
                            status=status)

    @view_config(route_name='cms_group', match_param='action=save-new',
                 renderer='json', request_method='POST')
    def save_new(self):
        _ = self.R
        print(_.params.get('name'))
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            if _.params.get('name', None) is not None:
                group = Group(_.params.get('name', None))
                _.db.add(group)
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)


class SeasonView(ZHandler):
    @view_config(route_name='cms_season', match_param='action=list',
                 renderer="cms/season/index.html")
    def index(self):
        _ = self.R
        cols_name = dict(id="ID", title="Season Title",
                         category="Category",
                         type="Season Type",
                         year="Season Years")

        data = dict(title="Master Season")

        return dict(project="season", cols=cols_name, data=data)

    @view_config(route_name='cms_season', match_param='action=src',
                 renderer='json', request_method="POST")
    def dataset(self):
        _ = self.R
        qry = Season.query

        season = qry.all()

        return dict(
            total=qry.count(),
            rows=[dict(id=sea.id,
                       title=sea.title,
                       category=sea.category, type=sea.type, year=sea.year) for sea in season]
        )

    @view_config(route_name='cms_season', match_param='action=edit-able',
                 renderer='json', request_method='POST')
    def editable_save(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Success'
            code, status = ResponseHTTP.OK
            qry = Season.query

            rdict = utils.loads(_.params.get("row", None))

            season = qry.get(rdict.get('id', None))
            season.title = rdict.get('title', '')
            season.slug = rdict.get('title', '')
            season.category = rdict.get('category', 'JD')
            season.type = rdict.get('type', 'winter')
            season.year = rdict.get('year', 0)

        return resp.to_json(_in,
                            code=code,
                            status=status)

    @view_config(route_name='cms_season', match_param='action=save-new',
                 renderer='json', request_method='POST')
    def save_new(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            if _.params.get('title', None) is not None:
                season = Season(
                    _.params.get('title', None),
                    _.params.get('category', 'JD'),
                    _.params.get('type', 'winter'),
                    _.params.get('year', 0))
                _.db.add(season)
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)


class SliderView(ZHandler):
    @view_config(route_name='cms_slider', match_param='action=list',
                 renderer="cms/slider/index.html")
    def index(self):
        _ = self.R

        cols_name = [FieldsGrid('id', 'ID', visible=False).to_dict(),
                     FieldsGrid('name', 'Slider Name', editable=True).to_dict(),
                     FieldsGrid('category', 'Slider Category', editable=dict(
                         type='select',
                         source=[{'value': 'JD', 'text': 'Dorama'},
                                 {'value': 'AN', 'text': 'Anime'},
                                 {'value': 'KD', 'text': 'KDrama'}])).to_dict(),
                     FieldsGrid('type', 'Slider Position', editable=dict(
                         type='select',
                         source=[{'value': 'HR', 'text': 'Header'},
                                 {'value': 'BT', 'text': 'Bottom'},
                                 {'value': 'MD', 'text': 'Middle'}])).to_dict(),
                     FieldsGrid('detail', 'Detail', width=50, align='left',
                                valign='middle',
                                actionable=dict(iconcls='fa fa-list-alt')).to_dict(),
                     FieldsGrid('delete', 'Delete', width=50, align='left',
                                valign='middle',
                                actionable=dict(iconcls='fa fa-trash-o')).to_dict()]

        data = dict(title="Master Images Slider")
        # print(utils.dumps(cols_name))

        return dict(project="slider", cols=utils.dumps(cols_name), data=data)

    @view_config(route_name='cms_slider', match_param='action=src',
                 renderer='json', request_method="POST")
    def dataset(self):
        _ = self.R
        qry = Slider.query

        slider = qry.all()

        return dict(
            total=qry.count(),
            rows=[dict(id=sld.id,
                       name=sld.name,
                       category=sld.category, type=sld.type) for sld in slider]
        )


    @view_config(route_name='cms_slider', match_param='action=edit-able',
                 renderer='json', request_method='POST')
    def editable_save(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Success'
            code, status = ResponseHTTP.OK
            qry = Slider.query

            rdict = utils.loads(_.params.get("row", None))

            slider = qry.get(rdict.get('id', None))
            slider.name = rdict.get('name', '')
            slider.slug = rdict.get('name', '')
            slider.category = rdict.get('category', 'JD')
            slider.type = rdict.get('type', 'HR')

        return resp.to_json(_in,
                            code=code,
                            status=status)

    @view_config(route_name='cms_slider', match_param='action=save-new',
                 renderer='json', request_method='POST')
    def save_new(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            if _.params.get('name', None) is not None:
                slider = Slider(
                    _.params.get('name', None),
                    _.params.get('category', 'JD'),
                    _.params.get('type', 'HR'))
                _.db.add(slider)
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)


class SliderDetailView(ZHandler):
    @view_config(route_name='cms_slider_detail', match_param='action=list',
                 renderer="cms/slider/detail.html")
    def index(self):
        _ = self.R

        cols_name = [FieldsGrid('id', 'ID', visible=False).to_dict(),
                     # master slider
                     FieldsGrid('pid', 'Slider Name',  editable=dict(
                         type='select',
                         source=[dict(value=slide.id, text=slide.name) for slide in Slider.query.all()])).to_dict(),
                     FieldsGrid('image', 'Image', editable=True).to_dict(),
                     FieldsGrid('url', 'Link Url', editable=True).to_dict(),
                     FieldsGrid('detail', 'Detail', width=50, align='left',
                                valign='middle',
                                actionable=dict(iconcls='fa fa-list-alt')).to_dict(),
                     FieldsGrid('delete', 'Delete', width=50, align='left',
                                valign='middle',
                                actionable=dict(iconcls='fa fa-trash-o')).to_dict()]

        sliders = [(slide.id, slide.name) for slide in Slider.query.all()]
        data = dict(title="List Images Slider", sliders=sliders)
        # print(utils.dumps(cols_name))

        return dict(project="slider", cols=utils.dumps(cols_name), data=data)

    @view_config(route_name='cms_slider_detail', match_param='action=src',
                 renderer='json', request_method="POST")
    def dataset(self):
        _ = self.R
        qry = SliderImage.query

        slider = qry.all()

        return dict(
            total=qry.count(),
            rows=[dict(id=sld.id,
                       name=sld.sliders.name,
                       image=sld.image, url=sld.url) for sld in slider]
        )

    @view_config(route_name='cms_slider_detail', match_param='action=edit-able',
                 renderer='json', request_method='POST')
    def editable_save(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Success'
            code, status = ResponseHTTP.OK
            qry = SliderImage.query

            rdict = utils.loads(_.params.get("row", None))
            slide = Slider.query.get(rdict.get("pid", None))
            sliderimg = qry.get(rdict.get('id', None))
            sliderimg.image = rdict.get('name', '')
            sliderimg.url = rdict.get('name', '')
            sliderimg.sliders = slide

        return resp.to_json(_in,
                            code=code,
                            status=status)

    @view_config(route_name='cms_slider_detail', match_param='action=save-new',
                 renderer='json', request_method='POST')
    def save_new(self):
        _ = self.R
        with ResponseHTTP(_.response) as resp:
            _in = u'Failed'
            code, status = ResponseHTTP.BAD_REQUEST
            print(_.POST['image'].filename)
            if _.params.get('image', None) is not None:
                slider = Slider.query.get(_.params.get('pid', 'HR'))
                slimage = SliderImage(
                    _.params.get('image', None),
                    _.params.get('url', 'JD'))
                slimage.sliders = slider
                _.db.add(slimage)
                _in = u'Success'
                code, status = ResponseHTTP.OK

        return resp.to_json(_in,
                            code=code,
                            status=status)