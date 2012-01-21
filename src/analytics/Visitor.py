

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
from datetime import datetime
import re

from analytics.internals import utils


class Visitor(object):
    """ 
    You should serialize this object and store it in the user database to keep it
    persistent for the same user permanently (similar to the "__umta" cookie of
    the GA Javascript client).

    @ivar unique_id:
        Unique user ID, will be part of the "__utma" cookie parameter

    @ivar first_visit_time:
        Time of the very first visit of this user, will be part of the "__utma" cookie parameter

    @ivar previous_visit_time:
        Time of the previous visit of this user, will be part of the "__utma" cookie parameter

    @ivar current_visit_time:
        Time of the current visit of this user, will be part of the "__utma" cookie parameter

    @ivar visit_count:
        Amount of total visits by this user, will be part of the "__utma" cookie parameter

    @ivar ip_address:
        IP Address of the end user, e.g. "123.123.123.123", will be mapped to "utmip"
        parameter and "X-Forwarded-For" request header

    @ivar user_agent:
        User agent string of the end user, will be mapped to "User-Agent" request header

    @ivar locale:
        Locale string (country part optional), e.g. "de-DE", will be mapped to "utmul" parameter

    @ivar flash_version:
        Visitor's Flash version, e.g. "9.0 r28", will be maped to "utmfl" parameter

    @ivar java_enabled:
        Visitor's Java support, will be mapped to "utmje" parameter

    @ivar screen_color_depth:
        Visitor's screen color depth, e.g. 32, will be mapped to "utmsc" parameter
        
    @ivar screen_resolution:
        Visitor's screen resolution, e.g. "1024x768", will be mapped to "utmsr" parameter
    """

    def __init__(self):
        """ 
        Creates a visitor without any previous visit information.
        """
        self.unique_id = None

        # ga.js sets all three timestamps to now for visitors, so we do the same
        now = datetime.now()
        self.first_visit_time = now 
        self.previous_visit_time = now
        self.current_visit_time = now

        self.visit_count = 1
        self.ip_address = None      
        self.user_agent = None      
        self.locale = None          
        self.flash_version = None   
        self.java_enabled = None    
        self.screen_color_depth = None
        self.screen_resolution = None


    def from_utma(self, value):
        """ 
        Will extract information for the "unique_id", "first_visit_time", "previous_visit_time",
        "current_visit_time" and "visit_count" properties from the given "__utma" cookie value.
        """
        parts = value.split('.')
        if len(parts) != 6:
            raise ValueError('The given "__utma" cookie value is invalid')
            #return self
        
        self.unique_id = parts[1]
        self.first_visit_time = datetime.fromtimestamp(parts[2])
        self.previous_visit_time = datetime.fromtimestamp(parts[3])
        self.current_visit_time = datetime.fromtimestamp(parts[4])
        self.visit_count = parts[5]
        
        # Allow chaining
        return self


    RE_VALID_IP_ADDR = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    RE_PRIVATE_IP_ADDR = re.compile(r'^(?:127\.0\.0\.1|10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.)')
    RE_LOCALES = re.compile(r'(^|\s,\s)([a-zA-Z]1,8(-[a-zA-Z]1,8))\s(\sq\s=\s(1(\.00,3)?|0(\.[0-9]0,3)))?', re.I)
    # http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4

    def from_server_var(self, environ):
        """ 
        Will extract information for the "ip_address", "user_agent" and "locale" properties
        from the given _SERVER variable.
        """
        if not environ.get('REMOTE_ADDR'):
            ip = None
            for key in ['X_FORWARDED_FOR', 'REMOTE_ADDR']:
                if environ.get(key) and not ip:
                    ips = environ[key].split(',')
                    ip  = ips[-1].strip()
                    
                    # Double-check if the address has a valid format
                    if not Visitor.RE_VALID_IP_ADDR.match(ip):
                        ip = None
                    
                    # Exclude private IP address ranges
                    if Visitor.RE_PRIVATE_IP_ADDR.match(ip):
                        ip = None
            if ip:
                self.ip_address = ip
        
        self.user_agent = environ.get('HTTP_USER_AGENT')
        
        if environ.get('HTTP_ACCEPT_LANGUAGE'):
            parsed_locales = {}
            res = Visitor.RE_LOCALES.match(environ['HTTP_ACCEPT_LANGUAGE'])
            if res:
                matches = list(res.groups())
                matches[2] = map(lambda part: part.replace('-','_'), matches[2])
                matches[5] = map(lambda part: 1 if part == '' else part, matches[5])
                parsed_locales = dict(zip(matches[2], matches[5]))
                
                # put biggest key from parsed_locales into self.locale
                # TODO verify with php-ga developers
                maxkey = max(parsed_locales.iterkeys(), key=float)
                self.locale = maxkey
        
        # Allow chaining
        return self


    def generate_hash(self):
        """ 
        Generates a hashed value from user-specific properties.
          
        @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Tracker.as#542
        @rtype int
        """
        # TODO: Emulate orginal Google Analytics client library generation more closely
        string = self.user_agent + self.screen_resolution + self.screen_color_depth
        return utils.generate_hash(string)


    def generate_unique_id(self):
        """ 
        Generates a unique user ID from the current user-specific properties.
          
        @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Tracker.as#563
        @rtype int
        """

        # There seems to be an error in the gaforflash code, so we take the formula
        # from http://xahlee.org/js/google_analytics_tracker_2010-07-01_expanded.js line 711
        # instead ("&" instead of "")
        return ((utils.generate_32bit_random() ^ self.generate_hash()) & 0x7fffffff)


    @property
    def unique_id(self):
        """ 
        Will be generated on first call (if not set already) to include as much
        user-specific information as possible.
        """
        if self.unique_id is None:
            self.unique_id = self.generate_unique_id()
        
        return self.unique_id

    @unique_id.setter
    def unique_id(self, value):
        if value < 0 or value > 0x7fffffff:
            raise ValueError('Visitor unique ID has to be a 32-bit integer between 0 and %d' % 0x7fffffff)
        
        self.unique_id = value


    def add_session(self, session):
        """ 
        Updates the "previous_visit_time", "current_visit_time" and "visit_count"
        fields based on the given session object.
          
        @param Session session
        """
        start_time = session.start_time
        if start_time != self.current_visit_time:
            self.previousVisitTime = self.current_visit_time
            self.current_visit_time  = start_time
            self.visit_count += 1
