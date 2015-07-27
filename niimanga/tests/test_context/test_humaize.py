"""
 # Copyright (c) 06 2015 | surya
 # 17/06/15 nanang.ask@kubuskotak.com
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
 #  test_humaize.py
"""
from datetime import datetime
from unittest import TestCase, main
import time

from niimanga.libs import utils
from niimanga.libs.utils import LocalDateTime


class HumanizeDate(TestCase):
    def test_normal(self):
        # print(datetime.fromtimestamp(1414524783))
        # dt = arrow.Arrow(2015, 6, 17, 13, 33, 3, tzinfo='+07:00')
        # dt = LocalDateTime.now()
        lt = LocalDateTime.now(tzinfo='+07:00')
        print(lt.humanize())
        # print(lt)
        # print(arrow.now())
        # print(dt.timestamp)
        # print(lt.timestamp)
        # ago = arrow.now().fromtimestamp(1414524783)
        # ago = arrow.now().fromtimestamp(lt.human_to_date_stamp('2 seconds ago'))
        # print(lt.fromtimestamp(lt.human_to_date_stamp('2 seconds ago')))
        nw = datetime.now()

        print lt.human_to_date('an year ago')
        print lt.human_to_date_stamp('now')
        print(LocalDateTime.from_time_stamp(lt.human_to_date_stamp('29 years ago')))

        print(nw)
        print(time.time())


class UtilHelpers(TestCase):
    def test_normal(self):
        name = "Vol.11 Ch.34: Kurase-san's Diary + Recipe 1 "
        c, v = utils.parse_number(name, "C"), utils.parse_number(name, "V")
        print(": ".join([c, v]))
        ext = "http://img.bato.to/forums/uploads/5aaa5b68168880d0e9724648baf4d808.png".lower().rsplit('.', 1)[-1]
        print(ext)


if __name__ == '__main__':
    main()