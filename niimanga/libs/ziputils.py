"""
 # Copyright (c) 07 2015 | surya
 # 08/07/15 nanang.ask@kubuskotak.com
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
 #  zipfile.py
"""
import datetime
import logging
from os import path, makedirs
import zipfile

LOG = logging.getLogger(__name__)


def print_info(archive_name):
    zf = zipfile.ZipFile(archive_name)
    for info in zf.infolist():
        print info.filename
        print '\tComment:\t', info.comment
        print '\tModified:\t', datetime.datetime(*info.date_time)
        print '\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)'
        print '\tZIP version:\t', info.create_version
        print '\tCompressed:\t', info.compress_size, 'bytes'
        print '\tUncompressed:\t', info.file_size, 'bytes'
        print


def extract_zip(archive_name, path_folder):
    try:
        print(path_folder)
        with zipfile.ZipFile(archive_name, "r") as zf:
            for info in zf.infolist():
                ifile = zf.read(info.filename)
                folder_zip = '/'.join([path_folder, info.filename.split('/')[-1]])
                if '.jpg' in folder_zip or '.png' in folder_zip:
                    # LOG.info(folder_zip)
                    if not path.exists(path_folder):
                        makedirs(path_folder)
                    with open(folder_zip, "wb") as img:
                        img.write(ifile)

        LOG.info(' '.join([archive_name, 'extract file success.']))
    except KeyError as e:
        LOG.info(e.message)
