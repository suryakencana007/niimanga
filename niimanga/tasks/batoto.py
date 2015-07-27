"""
 # Copyright (c) 06 2015 | surya
 # 26/06/15 nanang.ask@kubuskotak.com
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
 #  mangaeden.py
"""

# @app.task
# def build_idx_mongo(*args, **kwargs):
#     try:
#         mongo_index()
#         build_index_whoosh.delay()
#     except(KeyError, ValueError, AttributeError) as e:
#         LOG.error(e)
import shutil
from concurrent.futures import ThreadPoolExecutor
from niimanga.libs.exceptions import HtmlError
from niimanga.libs.utils import LocalDateTime
from niimanga.models.master import ISOLang
from os import path, makedirs

from niimanga.libs import utils
from niimanga.models.manga import Manga, Chapter
from .celery import load_ini
from niimanga.models.meta.base import initialize_sql, DBSession
import re
import requests
from requests.packages.urllib3.connection import ConnectionError
from requests_futures.sessions import FuturesSession
from sqlalchemy.exc import IntegrityError
import transaction


INI = load_ini()
initialize_sql(INI)

def _chapter_slug(str_, slug_manga):
    name = str_
    # print(name[name.index("C"):])
    no = re.search(r"\d+(\.\d+)?", name[name.index("C"):]).group(0)
    # print(no)
    return no, utils.slugist('{1}-chapter-{0}'.format(no.zfill(3), slug_manga))


def build_from_latest(site, source):
    try:
        lt = LocalDateTime.now()
        """
            dict(
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
        # list latest
        # scrap series info
        # url = "/".join([site.netlocs[2], source.get('origin')])
        url = source.get('origin')
        # print(url)
        respcontent = site.get_html(url)
        series_info = site.series_info(respcontent)

        # series == manga
        qry = Manga.query
        manga = qry.filter(Manga.slug == utils.slugist(
            "-".join([site.netlocs[4], source.get('name', None)])
        )).first()
        if manga is None:
            with transaction.manager:
                manga = Manga(
                    site.netlocs[4],
                    series_info.get('name', []),
                    0,
                    ", ".join(series_info.get('tags', [])),
                    ", ".join(series_info.get('authors', [])),
                    ", ".join(series_info.get('artists', [])),
                    ', '.join(series_info.get('aka', [])),
                    ",".join(series_info.get('description', None)),
                    1 if 'ongoing' in series_info.get('status', '').lower()
                    else 2 if 'completed' in series_info.get('status', '').lower() else 0
                )
                # manga.id = utils.guid()
                manga.origin = source.get('origin', '')
                manga.chapter_updated = lt.from_time_stamp(source.get('time', 'now'))
                ext = series_info.get('thumb_url', '').lower().rsplit('.', 1)[-1]
                manga.thumb = '.'.join(['cover', ext])
                manga.category = 'ja'
                DBSession.add(manga)
                DBSession.flush()

        manga = qry.filter(Manga.slug == utils.slugist(
            "-".join([site.netlocs[4], source.get('name', None)])
        )).first()
        manga_id, manga_thumb, manga_slug = manga.id, manga.thumb, manga.slug
        ini_path = path.join(
            path.dirname(
                path.dirname(__file__)
            ),
            '/'.join(['rak', 'manga', manga_id])
        )

        r = requests.get(source.get('thumb'))
        path_img = '/'.join([ini_path, manga_thumb])
        print(path_img)
        if not path.exists(ini_path):
            makedirs(ini_path)
        with open(path_img, "wb") as code:
            code.write(r.content)

        chapters_info = series_info.get('chapters', [])
        for i, ch in enumerate(chapters_info[0:2]):
            # batoto slug
            slug_bt = ch.get('name', '')

            if ':' in slug_bt:
                slug_bt = slug_bt.split(':')
                slug_bt.pop(0)
                slug_bt = '-'.join(slug_bt)

            slug_chapter = ' '.join([manga_slug, slug_bt])
            # cek chapter sudah didownload
            chapter = Chapter.query.filter(Chapter.slug == utils.slugist(slug_chapter)).first()
            if chapter is None:

                v = utils.parse_number(ch.get('name', ''), "Vol")
                v = 0 if v is None else v
                c = utils.parse_number(ch.get('name', ''), "Ch")
                c = 0 if c is None else c

                with transaction.manager:
                    chapter = Chapter(
                        slug_bt,
                        c,
                        v
                    )
                    time = lt.human_to_date(ch.get('time', 'now'))
                    # chapter.id = utils.guid()
                    ch_manga = Manga.query.get(manga_id)
                    ch_manga.chapter_count += 1
                    chapter.lang = ISOLang.query.filter(ISOLang.iso == 'en').first()
                    chapter.updated = time
                    chapter.manga = ch_manga
                    # s = 1000v + c
                    # chapter.sortorder = (1000*float(v)) + float(c)
                    chapter.sortorder = float(c)
                    chapter.slug = slug_chapter
                    DBSession.add(chapter)
                    DBSession.flush()

                chapter = Chapter.query.filter(Chapter.slug == utils.slugist(slug_chapter)).first()

                # batoto
                html = site.get_html(ch.get('url'))
                # # ambil image dan download locally di folder chapter.id
                chapter_info = site.chapter_info(html)
                try:
                    # series info
                    # chapter info and images
                    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))

                    for page in chapter_info.get('pages', []):
                        ini_chapter = '/'.join([ini_path, chapter.id])
                        print(page)
                        r = session.get(page).result()
                        if r.status_code != 200:
                            raise HtmlError('cannot fetch')
                        path_img = '/'.join([ini_chapter, page.split('/')[-1]])
                        print(path_img)
                        if not path.exists(ini_chapter):
                            makedirs(ini_chapter)
                        with open(path_img, "wb") as code:
                            code.write(r.content)
                except ConnectionError as Conn:
                    print(Conn)
                    chapter = Chapter.query.get(chapter.id)
                    DBSession.delete(chapter)
                    shutil.rmtree(ini_chapter)

    except AttributeError as e:
        print(e.message)
    except KeyError as e:
        print(e.message)
    except ValueError as e:
        print(e.message)


def build_from_latestDB():
    try:
        """
            dict(
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
        trans = transaction.begin()
        # manga = Manga(
        #     u'bt',
        #     u'Fairy Tail',
        #     0,
        #     u'comedy, shounen, adventure',
        #     u'Mushi shi',
        #     u'Hiro antsuki',
        #     u'False Love',
        #     u'Nisekoi'
        # )
        # manga.category = u'ja'
        # manga.save_it()
        manga = Manga.query.filter(Manga.slug == u'bt-fairy-tail').first()
        # DBSession.delete(manga)

        chapters = [
            {
                "name": "Ch.123: Without Fearing Spiciness",
                "url": "http://bato.to/read/_/327794/shokugeki-no-soma_ch123_by_casanova"
            },
            {
                "name": "Ch.122: \"M\u00e1\" and \"L\u00e0\"",
                "url": "http://bato.to/read/_/327793/shokugeki-no-soma_ch122_by_casanova"
            },
            {
                "name": "Ch.121: Spicy Flavor Worship",
                "url": "http://bato.to/read/_/325643/shokugeki-no-soma_ch121_by_casanova"
            },
            {
                "name": "Ch.120: What Is It!!?",
                "url": "http://bato.to/read/_/324650/shokugeki-no-soma_ch120_by_casanova"
            },
            {
                "name": "Ch.119: The Distance from the Elite Ten",
                "url": "http://bato.to/read/_/323145/shokugeki-no-soma_ch119_by_casanova"
            },
            {
                "name": "Ch.118: Tootsuki Elite Ten",
                "url": "http://bato.to/read/_/321978/shokugeki-no-soma_ch118_by_casanova"
            },
            {
                "name": "Ch.117.3 Read Online",
                "url": "http://bato.to/read/_/321119/shokugeki-no-soma_ch117.3_by_casanova"
            },
            {
                "name": "Ch.117: Imposingly",
                "url": "http://bato.to/read/_/321118/shokugeki-no-soma_ch117_by_casanova"
            },
            {
                "name": "Ch.116.5: A Magnificent Banquet",
                "url": "http://bato.to/read/_/318818/shokugeki-no-soma_ch116.5_by_casanova"
            },
            {
                "name": "Ch.116: The Fruit Called Growth",
                "url": "http://bato.to/read/_/318387/shokugeki-no-soma_ch116_by_casanova"
            },
            {
                "name": "Ch.115: Tear Through",
                "url": "http://bato.to/read/_/316969/shokugeki-no-soma_ch115_by_casanova"
            },
            {
                "name": "Ch.114: Yuihara (Revamped)",
                "url": "http://bato.to/read/_/316564/shokugeki-no-soma_ch114_by_casanova"
            },
            {
                "name": "Ch.113: Forgotten Vegetables",
                "url": "http://bato.to/read/_/314647/shokugeki-no-soma_ch113_by_casanova"
            },
            {
                "name": "Ch.112: The Guidepost for Growth",
                "url": "http://bato.to/read/_/314279/shokugeki-no-soma_ch112_by_casanova"
            },
            {
                "name": "Ch.111: Main Course",
                "url": "http://bato.to/read/_/312126/shokugeki-no-soma_ch111_by_casanova"
            },
            {
                "name": "Ch.110: The Magician, Once Again---!",
                "url": "http://bato.to/read/_/311083/shokugeki-no-soma_ch110_by_casanova"
            },
            {
                "name": "Ch.109: Those Who Shed Light",
                "url": "http://bato.to/read/_/309853/shokugeki-no-soma_ch109_by_casanova"
            },
            {
                "name": "Ch.108: Choosing a Path",
                "url": "http://bato.to/read/_/308448/shokugeki-no-soma_ch108_by_casanova"
            },
            {
                "name": "Ch.107: Ideals and Distance",
                "url": "http://bato.to/read/_/306749/shokugeki-no-soma_ch107_by_casanova"
            },
            {
                "name": "Ch.106: A Busy Restaurant with Many Problems",
                "url": "http://bato.to/read/_/305011/shokugeki-no-soma_ch106_by_casanova"
            },
            {
                "name": "Ch.105: Stagiaire",
                "url": "http://bato.to/read/_/303297/shokugeki-no-soma_ch105_by_casanova"
            },
            {
                "name": "Ch.104: New \"Jewel\"",
                "url": "http://bato.to/read/_/302063/shokugeki-no-soma_ch104_by_casanova"
            },
            {
                "name": "Ch.103: Specialty",
                "url": "http://bato.to/read/_/300229/shokugeki-no-soma_ch103_by_casanova"
            },
            {
                "name": "Ch.102: Souma's Strength",
                "url": "http://bato.to/read/_/299255/shokugeki-no-soma_ch102_by_casanova"
            },
            {
                "name": "Ch.101: A Fine Tempered Sword",
                "url": "http://bato.to/read/_/295858/shokugeki-no-soma_ch101_by_casanova"
            },
            {
                "name": "Ch.100: A Sharp Blade",
                "url": "http://bato.to/read/_/294443/shokugeki-no-soma_ch100_by_casanova"
            },
            {
                "name": "Ch.99: The Fangs That Cut Through The Battlefield",
                "url": "http://bato.to/read/_/293409/shokugeki-no-soma_ch99_by_casanova"
            },
            {
                "name": "Ch.98 (full color): The \"Things\" They've Accumulated",
                "url": "http://bato.to/read/_/292819/shokugeki-no-soma_ch98--full-color-_by_casanova"
            },
            {
                "name": "Ch.98: The \"Things\" They've Accumulated",
                "url": "http://bato.to/read/_/290601/shokugeki-no-soma_ch98_by_casanova"
            },
            {
                "name": "Ch.97 (full color): Moonlight Memories",
                "url": "http://bato.to/read/_/292818/shokugeki-no-soma_ch97--full-color-_by_casanova"
            },
            {
                "name": "Ch.97: Moonlight Memories",
                "url": "http://bato.to/read/_/289696/shokugeki-no-soma_ch97_by_casanova"
            },
            {
                "name": "Ch.96 (full color): The Answer He Reached",
                "url": "http://bato.to/read/_/292817/shokugeki-no-soma_ch96--full-color-_by_casanova"
            },
            {
                "name": "Ch.96: The Answer He Reached",
                "url": "http://bato.to/read/_/287642/shokugeki-no-soma_ch96_by_casanova"
            },
            {
                "name": "Ch.95 (full color): A Battle Surrounding the \"Season\"",
                "url": "http://bato.to/read/_/292816/shokugeki-no-soma_ch95--full-color-_by_casanova"
            },
            {
                "name": "Ch.95: A Battle Surrounding the \"Season\"",
                "url": "http://bato.to/read/_/286562/shokugeki-no-soma_ch95_by_casanova"
            },
            {
                "name": "Ch.94: Seizing the Season",
                "url": "http://bato.to/read/_/284514/shokugeki-no-soma_ch94_by_casanova"
            },
            {
                "name": "Ch.93: The \"Sword\" That Announces Autumn",
                "url": "http://bato.to/read/_/282575/shokugeki-no-soma_ch93_by_casanova"
            },
            {
                "name": "Ch.92: Firestarter",
                "url": "http://bato.to/read/_/280599/shokugeki-no-soma_ch92_by_casanova"
            },
            {
                "name": "Ch.91: Beats Eating Each Other",
                "url": "http://bato.to/read/_/279908/shokugeki-no-soma_ch91_by_casanova"
            },
            {
                "name": "Ch.90: Iron Will, Heart of Steel",
                "url": "http://bato.to/read/_/278692/shokugeki-no-soma_ch90_by_casanova"
            },
            {
                "name": "Ch.89: Morning Will Come Again",
                "url": "http://bato.to/read/_/277091/shokugeki-no-soma_ch89_by_casanova"
            },
            {
                "name": "Ch.88: ~DREAMLAND~",
                "url": "http://bato.to/read/_/275550/shokugeki-no-soma_ch88_by_casanova"
            },
            {
                "name": "Ch.87: Secret Plan",
                "url": "http://bato.to/read/_/274593/shokugeki-no-soma_ch87_by_casanova"
            },
            {
                "name": "Ch.86: Garniture",
                "url": "http://bato.to/read/_/272508/shokugeki-no-soma_ch86_by_casanova"
            },
            {
                "name": "Ch.85.2 Read Online",
                "url": "http://bato.to/read/_/271777/shokugeki-no-soma_ch85.2_by_casanova"
            },
            {
                "name": "Ch.85.1 Read Online",
                "url": "http://bato.to/read/_/271776/shokugeki-no-soma_ch85.1_by_casanova"
            },
            {
                "name": "Ch.85: The First Bite's Secret",
                "url": "http://bato.to/read/_/271775/shokugeki-no-soma_ch85_by_casanova"
            },
            {
                "name": "Ch.84: Hidden Assignment",
                "url": "http://bato.to/read/_/270967/shokugeki-no-soma_ch84_by_casanova"
            },
            {
                "name": "Ch.83: The Chaser And The Chased",
                "url": "http://bato.to/read/_/268312/shokugeki-no-soma_ch83_by_casanova"
            },
            {
                "name": "Ch.82: Starting Line",
                "url": "http://bato.to/read/_/265163/shokugeki-no-soma_ch82_by_casanova"
            },
            {
                "name": "Ch.81: The Observer Arrives",
                "url": "http://bato.to/read/_/263615/shokugeki-no-soma_ch81_by_casanova"
            },
            {
                "name": "Ch.80: The Conditions for the Challenge",
                "url": "http://bato.to/read/_/262016/shokugeki-no-soma_ch80_by_casanova"
            },
            {
                "name": "Ch.79: The Last \"Card\"",
                "url": "http://bato.to/read/_/259695/shokugeki-no-soma_ch79_by_casanova"
            },
            {
                "name": "Ch.78: A Paper-Thin Difference Between Offense and Defense",
                "url": "http://bato.to/read/_/258287/shokugeki-no-soma_ch78_by_casanova"
            },
            {
                "name": "Ch.77: Pursuer",
                "url": "http://bato.to/read/_/256463/shokugeki-no-soma_ch77_by_casanova"
            },
            {
                "name": "Ch.76: Duel Etiquette",
                "url": "http://bato.to/read/_/254889/shokugeki-no-soma_ch76_by_casanova"
            },
            {
                "name": "Ch.75: Beneath The Mask",
                "url": "http://bato.to/read/_/252716/shokugeki-no-soma_ch75_by_casanova"
            },
            {
                "name": "Ch.74: Sensitive Monster",
                "url": "http://bato.to/read/_/250870/shokugeki-no-soma_ch74_by_casanova"
            },
            {
                "name": "Ch.73: Minding The Details",
                "url": "http://bato.to/read/_/248966/shokugeki-no-soma_ch73_by_casanova"
            },
            {
                "name": "Ch.72: The \"Jewels\" Generation",
                "url": "http://bato.to/read/_/247956/shokugeki-no-soma_ch72_by_casanova"
            },
            {
                "name": "Ch.71: \"Courage\" and \"Resolution\"",
                "url": "http://bato.to/read/_/246285/shokugeki-no-soma_ch71_by_casanova"
            },
            {
                "name": "Ch.70: Polar Opposites",
                "url": "http://bato.to/read/_/245239/shokugeki-no-soma_ch70_by_casanova"
            },
            {
                "name": "Ch.69: Kitchen's Dictator",
                "url": "http://bato.to/read/_/243801/shokugeki-no-soma_ch69_by_casanova"
            },
            {
                "name": "Ch.68: The \"Port City\" Match",
                "url": "http://bato.to/read/_/241781/shokugeki-no-soma_ch68_by_casanova"
            },
            {
                "name": "Ch.67: Blending Light And Shadow",
                "url": "http://bato.to/read/_/239555/shokugeki-no-soma_ch67_by_casanova"
            },
            {
                "name": "Ch.66: What Fills That Box",
                "url": "http://bato.to/read/_/237502/shokugeki-no-soma_ch66_by_casanova"
            },
            {
                "name": "Ch.65: The Theory of Bento Evolution",
                "url": "http://bato.to/read/_/236405/shokugeki-no-soma_ch65_by_casanova"
            },
            {
                "name": "Ch.64: On the Edge",
                "url": "http://bato.to/read/_/234698/shokugeki-no-soma_ch64_by_casanova"
            },
            {
                "name": "Ch.63: Plan",
                "url": "http://bato.to/read/_/232844/shokugeki-no-soma_ch63_by_casanova"
            },
            {
                "name": "Ch.62: A Meeting of Strong People",
                "url": "http://bato.to/read/_/230838/shokugeki-no-soma_ch62_by_casanova"
            },
            {
                "name": "Ch.61: Putting Your Heart Into It",
                "url": "http://bato.to/read/_/228801/shokugeki-no-soma_ch61_by_casanova"
            },
            {
                "name": "Ch.60: The Warriors' Banquet",
                "url": "http://bato.to/read/_/227472/shokugeki-no-soma_ch60_by_casanova"
            },
            {
                "name": "Ch.59: Their Respective Weapons",
                "url": "http://bato.to/read/_/225853/shokugeki-no-soma_ch59_by_casanova"
            },
            {
                "name": "Ch.58: Holy Aroma",
                "url": "http://bato.to/read/_/224397/shokugeki-no-soma_ch58_by_casanova"
            },
            {
                "name": "Ch.57: Her Memories",
                "url": "http://bato.to/read/_/222875/shokugeki-no-soma_ch57_by_casanova"
            },
            {
                "name": "Ch.56: Tuscan Moon",
                "url": "http://bato.to/read/_/222555/shokugeki-no-soma_ch56_by_casanova"
            },
            {
                "name": "Ch.55: A Hole Drilled with Knowledge",
                "url": "http://bato.to/read/_/221797/shokugeki-no-soma_ch55_by_casanova"
            },
            {
                "name": "Ch.54: A Recital of Blossoming Individuals",
                "url": "http://bato.to/read/_/219111/shokugeki-no-soma_ch54_by_casanova"
            },
            {
                "name": "Ch.53: The Man Who Came From A Cold Country",
                "url": "http://bato.to/read/_/215047/shokugeki-no-soma_ch53_by_casanova"
            },
            {
                "name": "Ch.52.5: Natsuyumi no Erina",
                "url": "http://bato.to/read/_/213824/shokugeki-no-soma_ch52.5_by_casanova"
            },
            {
                "name": "Ch.52: Those Who Serve the Best",
                "url": "http://bato.to/read/_/211649/shokugeki-no-soma_ch52_by_casanova"
            },
            {
                "name": "Ch.51: The Witch's Dining Table",
                "url": "http://bato.to/read/_/211213/shokugeki-no-soma_ch51_by_casanova"
            },
            {
                "name": "Ch.50: Those Beyond Ordinary",
                "url": "http://bato.to/read/_/210069/shokugeki-no-soma_ch50_by_casanova"
            },
            {
                "name": "Ch.49: Wolf Pack",
                "url": "http://bato.to/read/_/208381/shokugeki-no-soma_ch49_by_casanova"
            },
            {
                "name": "Ch.48: The Known Unknown",
                "url": "http://bato.to/read/_/207413/shokugeki-no-soma_ch48_by_casanova"
            },
            {
                "name": "Ch.47: Battle Memories",
                "url": "http://bato.to/read/_/205556/shokugeki-no-soma_ch47_by_casanova"
            },
            {
                "name": "Ch.46: The Dragon Lies Down and then Ascends to the Sky",
                "url": "http://bato.to/read/_/203799/shokugeki-no-soma_ch46_by_casanova"
            },
            {
                "name": "Ch.45: The Accompanist of Aromas and Stimuli",
                "url": "http://bato.to/read/_/202784/shokugeki-no-soma_ch45_by_casanova"
            },
            {
                "name": "Ch.44: An Unexpected Straight",
                "url": "http://bato.to/read/_/201764/shokugeki-no-soma_ch44_by_casanova"
            },
            {
                "name": "Ch.43: The Cook Who Has Travelled Thousands of Miles",
                "url": "http://bato.to/read/_/200010/shokugeki-no-soma_ch43_by_casanova"
            },
            {
                "name": "Ch.42: Wake Up Kiss",
                "url": "http://bato.to/read/_/199003/shokugeki-no-soma_ch42_by_casanova"
            },
            {
                "name": "Ch.41: The Man Who was Called an \"Asura\"",
                "url": "http://bato.to/read/_/196809/shokugeki-no-soma_ch41_by_casanova"
            },
            {
                "name": "Ch.40: Return",
                "url": "http://bato.to/read/_/195573/shokugeki-no-soma_ch40_by_casanova"
            },
            {
                "name": "Ch.39: The Chosen Ones",
                "url": "http://bato.to/read/_/192744/shokugeki-no-soma_ch39_by_casanova"
            },
            {
                "name": "Ch.38: Sensual Karaage (4)",
                "url": "http://bato.to/read/_/192097/shokugeki-no-soma_ch38_by_casanova"
            },
            {
                "name": "Ch.37: Sensual Karaage (3)",
                "url": "http://bato.to/read/_/190617/shokugeki-no-soma_ch37_by_casanova"
            },
            {
                "name": "Ch.36v2: Sensual Kaarage (2)",
                "url": "http://bato.to/read/_/189007/shokugeki-no-soma_ch36v2_by_casanova"
            },
            {
                "name": "Ch.35.5: Mid-Summer's Nikumi-san",
                "url": "http://bato.to/read/_/188961/shokugeki-no-soma_ch35.5_by_casanova"
            },
            {
                "name": "Ch.35: Sensual Karaage (1)",
                "url": "http://bato.to/read/_/186597/shokugeki-no-soma_ch35_by_casanova"
            },
            {
                "name": "Ch.34: The Fate Surrounding Tootsuki",
                "url": "http://bato.to/read/_/185446/shokugeki-no-soma_ch34_by_casanova"
            },
            {
                "name": "Ch.33: To the People that will Eventually Fight",
                "url": "http://bato.to/read/_/184581/shokugeki-no-soma_ch33_by_casanova"
            },
            {
                "name": "Ch.32: Dancing Cook",
                "url": "http://bato.to/read/_/183357/shokugeki-no-soma_ch32_by_casanova"
            },
            {
                "name": "Ch.31: Metamorphose",
                "url": "http://bato.to/read/_/182129/shokugeki-no-soma_ch31_by_casanova"
            },
            {
                "name": "Ch.30: A Set Trap",
                "url": "http://bato.to/read/_/180945/shokugeki-no-soma_ch30_by_casanova"
            },
            {
                "name": "Ch.29: The Eggs Before Dawn",
                "url": "http://bato.to/read/_/179806/shokugeki-no-soma_ch29_by_casanova"
            },
            {
                "name": "Ch.28: Everyone Must Not Fall Asleep",
                "url": "http://bato.to/read/_/178134/shokugeki-no-soma_ch28_by_casanova"
            },
            {
                "name": "Ch.27: The Bitterness of Defeat",
                "url": "http://bato.to/read/_/177135/shokugeki-no-soma_ch27_by_casanova"
            },
            {
                "name": "Ch.26: Memories of a Dish",
                "url": "http://bato.to/read/_/176297/shokugeki-no-soma_ch26_by_casanova"
            },
            {
                "name": "Ch.25: Those Remnants",
                "url": "http://bato.to/read/_/174116/shokugeki-no-soma_ch25_by_casanova"
            },
            {
                "name": "Ch.24: The Magician that Came from the East",
                "url": "http://bato.to/read/_/173475/shokugeki-no-soma_ch24_by_casanova"
            },
            {
                "name": "Ch.23: Proof of Existence",
                "url": "http://bato.to/read/_/171105/shokugeki-no-soma_ch23_by_casanova"
            },
            {
                "name": "Ch.22: Alumni",
                "url": "http://bato.to/read/_/170355/shokugeki-no-soma_ch22_by_casanova"
            },
            {
                "name": "Ch.21: The Supreme Recette",
                "url": "http://bato.to/read/_/167841/shokugeki-no-soma_ch21_by_casanova"
            },
            {
                "name": "Ch.20: Verdict",
                "url": "http://bato.to/read/_/166990/shokugeki-no-soma_ch20_by_casanova"
            },
            {
                "name": "Ch.19: Sparkling Soul",
                "url": "http://bato.to/read/_/165823/shokugeki-no-soma_ch19_by_casanova"
            },
            {
                "name": "Ch.18: The Seed of Ideas",
                "url": "http://bato.to/read/_/165444/shokugeki-no-soma_ch18_by_casanova"
            },
            {
                "name": "Ch.17: The Coating that Colors the Mountain",
                "url": "http://bato.to/read/_/164819/shokugeki-no-soma_ch17_by_casanova"
            },
            {
                "name": "Vol.3 Ch.16.5 Read Online",
                "url": "http://bato.to/read/_/213776/shokugeki-no-soma_v3_ch16.5_by_casanova"
            },
            {
                "name": "Ch.16: Concerto of Ideas and Creation",
                "url": "http://bato.to/read/_/162138/shokugeki-no-soma_ch16_by_casanova"
            },
            {
                "name": "Ch.15: Friction and Elite",
                "url": "http://bato.to/read/_/161276/shokugeki-no-soma_ch15_by_casanova"
            },
            {
                "name": "Vol.2 Ch.14.5: Volume 2 Extra and Recipes",
                "url": "http://bato.to/read/_/209555/shokugeki-no-soma_v2_ch14.5_by_casanova"
            },
            {
                "name": "Ch.14: Megumi's Garden",
                "url": "http://bato.to/read/_/160292/shokugeki-no-soma_ch14_by_casanova"
            },
            {
                "name": "Ch.13: Quiet Don, An Eloquent Don",
                "url": "http://bato.to/read/_/159427/shokugeki-no-soma_ch13_by_casanova"
            },
            {
                "name": "Ch.12: Enter the Battlefield",
                "url": "http://bato.to/read/_/158233/shokugeki-no-soma_ch12_by_casanova"
            },
            {
                "name": "Ch.11: The Night Before the Showdown",
                "url": "http://bato.to/read/_/157118/shokugeki-no-soma_ch11_by_casanova"
            },
            {
                "name": "Ch.10: The Meat Invader",
                "url": "http://bato.to/read/_/155824/shokugeki-no-soma_ch10_by_casanova"
            },
            {
                "name": "Ch.9: The Ice Queen and the Spring Storm",
                "url": "http://bato.to/read/_/154910/shokugeki-no-soma_ch9_by_casanova"
            },
            {
                "name": "Ch.8: A Dish that Calls for Spring",
                "url": "http://bato.to/read/_/153806/shokugeki-no-soma_ch8_by_casanova"
            },
            {
                "name": "Ch.7: Lawless Area",
                "url": "http://bato.to/read/_/153114/shokugeki-no-soma_ch7_by_casanova"
            },
            {
                "name": "Ch.6: Maria of the Polar Star",
                "url": "http://bato.to/read/_/149043/shokugeki-no-soma_ch6_by_casanova"
            },
            {
                "name": "Ch.5: The Chef That Doesn't Smile",
                "url": "http://bato.to/read/_/147981/shokugeki-no-soma_ch5_by_casanova"
            },
            {
                "name": "Ch.4.5: Kurase-san's Diary + Recipe 1",
                "url": "http://bato.to/read/_/199090/shokugeki-no-soma_ch4.5_by_casanova"
            },
            {
                "name": "Ch.4: The Demon King Talks About \"Gems\"",
                "url": "http://bato.to/read/_/146795/shokugeki-no-soma_ch4_by_casanova"
            },
            {
                "name": "Ch.3: \"Transforming Furikake\"",
                "url": "http://bato.to/read/_/146229/shokugeki-no-soma_ch3_by_casanova"
            },
            {
                "name": "Ch.2: God's Tounge",
                "url": "http://bato.to/read/_/144856/shokugeki-no-soma_ch2_by_casanova"
            },
            {
                "name": "Ch.1: The Endless Wilderness",
                "url": "http://bato.to/read/_/143718/shokugeki-no-soma_ch1_by_casanova"
            },
            {
                "name": "Ch.0: [Oneshot]",
                "url": "http://bato.to/read/_/182841/shokugeki-no-soma_by_utopia"
            }
        ]

        for i, ch in enumerate(chapters):
            # eden
            # url = "/".join([site.netlocs[2], ch.get('url')])
            # html = site.get_html(url)
            # site.chapter_info(html)
            v = utils.parse_number(ch.get('name', ''), "Vol")
            v = 0 if v is None else v
            c = utils.parse_number(ch.get('name', ''), "Ch")
            c = 0 if c is None else c
            try:
                chapter = Chapter(
                    ch.get('name', '').split(':')[-1],
                    c,
                    v
                )
                chapter.id = utils.guid()
                chapter.slug = " ".join([manga.slug, ch.get('name', '').split(':')[0]])
                chapter.manga = manga
                # s = 1000v + c
                chapter.sortorder = (1000*float(v)) + float(c)
                chapter.save_it()

                print(chapter.id)
                ini_path = path.join(
                    path.dirname(
                        path.dirname(__file__)
                    ),
                    '/'.join(['rak', 'manga', chapter.id])
                )
                print(ini_path)

            except IntegrityError as IE:
                print(IE.message)
                # if 'violates unique constraint' in IE.message:
                #     c += float(c / 100)
                #     chapter = Chapter(
                #         ch.get('name', '').split(':')[-1],
                #         manga.slug,
                #         c,
                #         v
                #     )
                #     chapter.manga = manga
                #     # s = 1000v + c
                #     print("{0}: {1}".format(v, c))
                #     chapter.sortorder = (1000*float(v)) + float(c)
                #     chapter.save_it()

        trans.commit()
    except AttributeError as e:
        print(e.message)
    except KeyError as e:
        print(e.message)
    except ValueError as e:
        print(e.message)
