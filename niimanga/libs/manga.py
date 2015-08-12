"""
 # Copyright (c) 04 2015 | surya
 # 20/04/15 nanang.ask@kubuskotak.com
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
import logging

import os
from natsort import natsorted


LOG = logging.getLogger(__name__)


class MangaUtil(object):

    items = None

    def __init__(self, dirpath=".", manga="", chapter=""):
        self.path = os.path.join(dirpath, manga, chapter)

    def get_image_names(self):
        # The top argument for name in files
        extens = ['jpg', 'png', 'gif']  # the extensions to search for
        names = []
        # LOG.debug(self.path)
        for root, dirs, files in os.walk(self.path):
            # Loop through the file names for the current step
            for name in files:
                # Split the name by '.' & get the last element
                ext = name.lower().rsplit('.', 1)[-1]

                # Save the full name if ext matches
                if ext in extens:
                    # names.append(os.path.join(self.path, name))
                    # print(os.path.join(dirname, filename))
                    names.append(name)
                # LOG.debug('{dirs}-{files}'.format(dirs=dirs, files=name))
        return names

    def build_image_lookup_dict(self):
        names = natsorted(self.get_image_names())
        self.items = dict(zip(range(len(names)), names))

    def get_keys(self):
        try:
            keys = list(self.items.keys())
            return keys

        except AttributeError:
            raise ValueError("No Images in archive! \n Archive contents = %s" % "\n		".join(self.path))

    def get_item_by_key(self, itemkey):
        if not itemkey in self.items:
            raise KeyError("Invalid key. Not in archive!")

        internalpath = self.items[itemkey]
        # itemcontent = self.archHandle.open(internalpath)
        return itemkey, internalpath

    def __del__(self):
        pass


def parse_chapter(chapter):
    # e.g Chapter-010
    return int(str(chapter).lower().rsplit('-', 1)[-1])