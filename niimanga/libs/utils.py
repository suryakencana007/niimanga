"""
 # Copyright (c) 03 2015 | surya
 # 12/03/15 nanang.ask@kubuskotak.com
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
 #  utils.py
"""
from datetime import datetime, date, timedelta
import hashlib
import hmac
import json
import logging
from decimal import Decimal
import random
import string
import urllib
import time

from arrow import arrow
from formencode.validators import Number, Invalid
import re
from slugify import slugify


log = logging.getLogger(__name__)

ACCESS_TOKEN_LENGTH = 32
REFRESH_TOKEN_LENGTH = 32
CLIENT_KEY_LENGTH = 40
CLIENT_SECRET_LENGTH = 20
ALLOWED_CHARACTERS = string.letters + string.digits + '-' + '.' + '_' + '~'
URI_API = u'/api/v1'
MANGA_PATH = u'rak/manga/'
ANIME_PATH = u'rak/anime/'


class DecimalNumber(Number):
    """formencode validator for Decimal objects."""

    def _to_python(self, value, state):
        try:
            value = Decimal(value)
            return value
        except ValueError:
            raise Invalid(self.message('number', state), value, state)


def dumps(obj, default=None, **kw):
    """Json dumps function which includes Decimal processing as well as logging."""

    def default_(obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif default is not None:
            return default(obj)
        else:
            raise TypeError("value not json encodable: %s" % obj)
    dumped = json.dumps(obj, default=default_, indent=4, **kw)
    log.debug(dumped)
    return dumped


def loads(obj):
    """Json Loads to dict"""
    return json.loads(obj)


def quote(s):
    """fungsi filter qoute urllib """
    return urllib.quote(s, safe=ALLOWED_CHARACTERS)


def nonce(n):
    return ''.join(random.choice(ALLOWED_CHARACTERS) for i in range(n))


def hmacsha1(key, signature_base):
    hm = hmac.new(key, signature_base, hashlib.sha1)
    return hm.digest().encode('base64').strip()


def hmacsha256(key, signature_base):
    hm = hmac.new(key, signature_base, hashlib.sha256)
    return hm.hexdigest().encode('base64').strip()


def timestamp():
    return int(time.time())

# def genid():
#     return int(str(int(str(timestamp())[:4])
#                    + datetime.now().second
#                    + datetime.now().minute)
#                + str(timestamp())[4:])


def genid():
    return int(timestamp())


def guid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t = long(time.time() * 1000)
    r = long(random.random()*100000000000000000L)

    a = random.random()*100000000000000000L
    data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    data = hashlib.md5(data).hexdigest()[:10]

    return data


# untuk parsing angka vol atau chapter
def parse_number(str_, split_str):
    try:
        # print(str_)
        # split_str, str_ = split_str.lower(), str_.lower()
        group = re.search(r"\d+(\.\d+)?", str_[str_.index(split_str):])
        return group.group(0)
    except ValueError:
        return None
    except TypeError:
        return 0


def slugist(str):
    return slugify(str, to_lower=True)


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs


class ResponseHTTP(Timer):
    """
        200 OK - Success
        400 Bad Request - The request was invalid.
        401 Not Authorized - Authentication credentials were missing or invalid.
        403 Forbidden - The request was understood, but it has been refused for some reason.
        404 Not Found - The requested URI does not exist.
        500 Internal Server Error - Some unexpected error has occurred.
        503 Service Unavailable - The API is currently not online
    """
    OK = (200, "OK")
    BAD_REQUEST = (400, "BAD REQUEST")
    NOT_AUTHORIZED = (401, "NOT AUTHORIZED")
    FORBIDDEN = (403, "FORBIDDEN")
    NOT_FOUND = (404, "NOT FOUND")
    INTERNAL_SERVER_ERROR = (500, "INTERNAL SERVER ERROR")
    SERVICE_UNAVAILABLE = (503, "SERVICE UNAVAILABLE")

    def __init__(self, response=None):
        self.Resp = response
        super(ResponseHTTP, self).__init__()

    def to_json(self, confirm, **kwargs):
        code = kwargs.pop("code", ResponseHTTP.OK[0])
        self.Resp.status_code = code
        self.__dict__ = {
            "response": {
                "status": code,
                "description": kwargs.pop("status", ResponseHTTP.OK[1]),
                "elapsetime": float(format(self.msecs, '.4f')),
                # optional "memoryusage": kwargs.pop("ram", "0 MB"),
                "unix_timestamp": timestamp(),
                "confirm": confirm,
                "lang": "id",
                "currency": "IDR"
            }
        }
        self.__dict__.update(kwargs)
        # self.__dict__.update(args)
        return self.__dict__


class FieldsGrid(object):
    """
        'field': '',
        'title': '',
        'sortable': True,
        'visible': True,
    """
    def __init__(self, field, title, **kwargs):
        self.field = field
        self.title = title
        self.sortable = True
        self.visible = True
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return dumps(self.__dict__)

    def __repr__(self):
        return dumps(self.__dict__)

try: # pragma: no cover
    basestring

    def isstr(s):
        return isinstance(s, basestring)

except NameError: #pragma: no cover

    def isstr(s):
        return isinstance(s, str)


class LocalDateTime(arrow.Arrow):
    def __sub__(self, other):
        pass

    def __add__(self, other):
        pass

    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0,
                 tzinfo=None):
        super(LocalDateTime, self).__init__(year, month, day, hour, minute, second, microsecond,
                                            tzinfo=tzinfo)

    def human_to_date(self, dtstr):
        delta = re.findall(r"[\d+]+", dtstr)
        if 'now' in dtstr:
            diff = 0
        elif 'seconds' in dtstr:
            diff = int(delta[0]) if len(delta) > 0 else 45
        elif 'minutes' in dtstr:
            # 2700
            diff = int(delta[0])*60
        elif 'minute' in dtstr:
            diff = 90
        elif 'hours' in dtstr:
            # 79200
            diff = int(delta[0])*3600
        elif 'hour' in dtstr:
            diff = 5400
        elif 'days' in dtstr:
            # 2160000
            diff = int(delta[0])*86400
        elif 'day' in dtstr:
            diff = 129600
        elif 'weeks' in dtstr:
            diff = int(delta[0])*7*86400
        elif 'week' in dtstr:
            diff = 7*86400
        elif 'months ago' in dtstr:
            # 29808000
            days = (self._datetime.date() -
                    date(self._datetime.year,
                         (self._datetime.month - int(delta[0])), 1)).days
            diff = days*86400
        elif 'month' in dtstr:
            diff = 3888000
        elif 'years' in dtstr:
            diff = int(delta[0])*31536000
        elif 'year' in dtstr:
            diff = 47260800
        else:
            # batoto 17 May 2015 - 07:28 PM replace if there [A]
            if '[A]' in dtstr:
                print(dtstr)
                dtstr = dtstr.replace("[A]", '')
            return datetime.strptime(dtstr.strip(), "%d %B %Y - %I:%M %p")

        if 'ago' in dtstr:
            diff = -diff

        return self._datetime + timedelta(seconds=diff)

    def human_to_date_stamp(self, dtstr):
        result = self.human_to_date(dtstr)
        return time.mktime(result.timetuple())

    @staticmethod
    def from_time_stamp(timestamp):
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def to_time_stamp(timetuple):
        return time.mktime(timetuple)