

""" 
Generic Server-Side Google Analytics PHP Client

This library is free software you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License (LGPL) as published by the Free Software Foundation either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.

Google Analytics is a registered trademark of Google Inc.

@link      http://code.google.com/p/php-ga

@license   http://www.gnu.org/licenses/lgpl.html
@author    Thomas Bachem <tb@unitedprototype.com>
@copyright Copyright (c) 2010 United Prototype GmbH (http://unitedprototype.com)
"""

""" 
@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/Utils.as
"""

import random
import urllib
import time


""" 
Mimics Javascript's encodeURIComponent() def for consistency with the GA Javascript client.

@param mixed value
@return string
"""
def encodeUriComponent(value):
    return convertToUriComponentEncoding(urllib.quote(value))


""" 
Here as a separate method so it can also be applied to e.g. a http_build_query() result.

@link http://stackoverflow.com/questions/1734250/what-is-the-equivalent-of-javascripts-encodeuricomponent-in-php/1734255#1734255
@link http://devpro.it/examples/php_js_escaping.php

@param string encodedValue
@return string
"""

URI_COMPONENT_ENCODING = {'%21': '!', '%2A': '*', '%27': "'", '%28': '(', '%29': ')'}

def convertToUriComponentEncoding(encodedValue):
    return replace_all(encodedValue, URI_COMPONENT_ENCODING)


""" 
Generates a 32bit random number.

@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/Utils.as#33
@return int
"""
def generate32bitRandom():
    return random.getrandbits(32)


""" 
Generates a hash for input string.

@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/Utils.as#44
@param string string
@return int
"""
def generateHash(string):
    hashval = 1
    
    if string:
        hashval = 0
        length = len(string)
        for pos in range(length-1, -1, -1):
            current   = ord(string[pos])
            hashval      = ((hashval << 6) & 0xfffffff) + current + (current << 14)
            leftMost7 = hashval & 0xfe00000
            if leftMost7 != 0:
                hashval ^= leftMost7 >> 21
    
    return hashval



def replace_all(text, dic):
    for old, new in dic.iteritems():
        text = text.replace(old, new)
    return text


def totimestamp(d):
    return time.mktime(d.timetuple())