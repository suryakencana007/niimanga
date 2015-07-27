"""
 # Copyright (c) 06 2015 | surya
 # 22/06/15 nanang.ask@kubuskotak.com
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
 #  manga.py
"""
from niimanga.models.manga import Manga


class MangaService(object):

    @staticmethod
    def insert_scrap_data(objs):
        """
        {
             "origin": "http://bato.to/comic/_/comics/youkai-shoujo-monsuga-r11767",
             "last_chapter": " Ch.39: The wind has died down...",
             "name": "Youkai Shoujo - Monsuga",
             "time": 1434953127.0,
             "last_url": "http://bato.to/read/_/328045/youkai-shoujo-monsuga_ch39_by_japanzai",
             "site": "batoto",
             "thumb": "http://img.bato.to/forums/uploads/6a258c7c65ea8478d0fb28e23964462b.jpg"
         }
        :param objs:
        :return:
        """
        manga = Manga()