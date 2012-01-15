

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

from googleanalytics.internals import utils

""" 
You should serialize this object and store it in the user database to keep it
persistent for the same user permanently (similar to the "__umta" cookie of
the GA Javascript client).
"""
class Visitor(object):

    """ 
    Unique user ID, will be part of the "__utma" cookie parameter

    @see Internals\ParameterHolder::__utma
    @var int
    """

    """ 
    Time of the very first visit of this user, will be part of the "__utma"
    cookie parameter

    @see Internals\ParameterHolder::__utma
    @var DateTime
    """

    """ 
    Time of the previous visit of this user, will be part of the "__utma"
    cookie parameter

    @see Internals\ParameterHolder::__utma
    @see addSession
    @var DateTime
    """

    """ 
    Time of the current visit of this user, will be part of the "__utma"
    cookie parameter

    @see Internals\ParameterHolder::__utma
    @see addSession
    @var DateTime
    """

    """ 
    Amount of total visits by this user, will be part of the "__utma"
    cookie parameter

    @see Internals\ParameterHolder::__utma
    @var int
    """

    """ 
    IP Address of the end user, e.g. "123.123.123.123", will be mapped to "utmip" parameter
    and "X-Forwarded-For" request header

    @see Internals\ParameterHolder::utmip
    @see Internals\Request\HttpRequest::xForwardedFor
    @var string
    """

    """ 
    User agent string of the end user, will be mapped to "User-Agent" request header

    @see Internals\Request\HttpRequest::userAgent
    @var string
    """

    """ 
    Locale string (country part optional), e.g. "de-DE", will be mapped to "utmul" parameter

    @see Internals\ParameterHolder::utmul
    @var string
    """

    """ 
    Visitor's Flash version, e.g. "9.0 r28", will be maped to "utmfl" parameter

    @see Internals\ParameterHolder::utmfl
    @var string
    """

    """ 
    Visitor's Java support, will be mapped to "utmje" parameter

    @see Internals\ParameterHolder::utmje
    @var bool
    """

    """ 
    Visitor's screen color depth, e.g. 32, will be mapped to "utmsc" parameter

    @see Internals\ParameterHolder::utmsc
    @var string
    """

    """ 
    Visitor's screen resolution, e.g. "1024x768", will be mapped to "utmsr" parameter

    @see Internals\ParameterHolder::utmsr
    @var string
    """
    """ 
    Creates a visitor without any previous visit information.
    """
    def __init__(self):
        self.uniqueId = None
        self.firstVisitTime = None
        self.previousVisitTime = None
        self.currentVisitTime = None
        self.visitCount = None
        self.ipAddress = None
        self.userAgent = None
        self.locale = None
        self.flashVersion = None
        self.javaEnabled = None
        self.screenColorDepth = None
        self.screenResolution = None
        
        # ga.js sets all three timestamps to now for visitors, so we do the same
        now = datetime.now()
        self.setFirstVisitTime(now)
        self.setPreviousVisitTime(now)
        self.setCurrentVisitTime(now)
        
        self.setVisitlen(1)


    """ 
      Will extract information for the "uniqueId", "firstVisitTime", "previousVisitTime",
    "currentVisitTime" and "visitCount" properties from the given "__utma" cookie
      value.
      
    @see Internals\ParameterHolder::__utma
    @see Internals\Request\Request::buildCookieParameters()
    @param string value
    @return this
    """
    def fromUtma(self, value):
        parts = value.split('.')
        if len(parts) != 6:
            raise ValueError('The given "__utma" cookie value is invalid')
            #return self
        
        self.setUniqueId(parts[1])
        self.setFirstVisitTime(datetime.fromtimestamp(parts[2]))
        self.setPreviousVisitTime(datetime.fromtimestamp(parts[3]))
        self.setCurrentVisitTime(datetime.fromtimestamp(parts[4]))
        self.setVisitlen(parts[5])
        
        # Allow chaining
        return self


    """ 
      Will extract information for the "ipAddress", "userAgent" and "locale" properties
      from the given _SERVER variable.
      
    @param array value
    @return this
    """
    RE_VALID_IP_ADDR = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    RE_PRIVATE_IP_ADDR = re.compile(r'^(?:127\.0\.0\.1|10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.)')
    RE_LOCALES = re.compile(r'(^|\s,\s)([a-zA-Z]1,8(-[a-zA-Z]1,8))\s(\sq\s=\s(1(\.00,3)?|0(\.[0-9]0,3)))?', re.I)
    # http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4
    def fromServerVar(self, value):
        if not value['REMOTE_ADDR']:
            ip = None
            for key in ['X_FORWARDED_FOR', 'REMOTE_ADDR']:
                if value[key] and not ip:
                    ips = value[key].split(',')
                    ip  = ips[-1].strip()
                    
                    # Double-check if the address has a valid format
                    if not Visitor.RE_VALID_IP_ADDR.match(ip):
                        ip = None
                    
                    # Exclude private IP address ranges
                    if Visitor.RE_PRIVATE_IP_ADDR.match(ip):
                        ip = None
            if ip:
                self.setIpAddress(ip)
        
        if value.get('HTTP_USER_AGENT'):
            self.setUserAgent(value['HTTP_USER_AGENT'])
        
        if value.get('HTTP_ACCEPT_LANGUAGE'):
            parsedLocales = {}
            res = Visitor.RE_LOCALES.match(value['HTTP_ACCEPT_LANGUAGE'])
            if res:
                matches = list(res.groups())
                matches[2] = map(lambda part: part.replace('-','_'), matches[2])
                matches[5] = map(lambda part: 1 if part == '' else part, matches[5])
                parsedLocales = dict(zip(matches[2], matches[5]))
                
                # put biggest key from parsedLocales into self.locale
                # TODO verify with php-ga developers
                maxkey = max(parsedLocales.iterkeys(), key=float)
                self.setLocale(maxkey)
        
        # Allow chaining
        return self


    """ 
      Generates a hashed value from user-specific properties.
      
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Tracker.as#542
    @return int
    """
    def generateHash(self):
        # TODO: Emulate orginal Google Analytics client library generation more closely
        string = self.userAgent + self.screenResolution + self.screenColorDepth
        return utils.generateHash(string)


    """ 
      Generates a unique user ID from the current user-specific properties.
      
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Tracker.as#563
    @return int
    """
    def generateUniqueId(self):
        # There seems to be an error in the gaforflash code, so we take the formula
        # from http://xahlee.org/js/google_analytics_tracker_2010-07-01_expanded.js line 711
        # instead ("&" instead of "")
        return ((utils.generate32bitRandom() ^ self.generateHash()) & 0x7fffffff)


    """ 
    @see generateUniqueId
    @param int value
    """
    def setUniqueId(self, value):
        if value < 0 or value > 0x7fffffff:
            raise ValueError('Visitor unique ID has to be a 32-bit integer between 0 and %d' % 0x7fffffff)
        
        self.uniqueId = value


    """ 
      Will be generated on first call (if not set already) to include as much
      user-specific information as possible.
      
    @return int
    """
    def getUniqueId(self):
        if self.uniqueId is None:
            self.uniqueId = self.generateUniqueId()
        
        return self.uniqueId


    """ 
      Updates the "previousVisitTime", "currentVisitTime" and "visitCount"
      fields based on the given session object.
      
    @param Session session
    """
    def addSession(self, session):
        startTime = session.getStartTime()
        if startTime != self.currentVisitTime:
            self.previousVisitTime = self.currentVisitTime
            self.currentVisitTime  = startTime
            self.visitCount += 1
        
    """ 
    @param DateTime value
    """
    def setFirstVisitTime(self, value):
        self.firstVisitTime = value


    """ 
    @return DateTime
    """
    def getFirstVisitTime(self):
        return self.firstVisitTime


    """ 
    @param DateTime value
    """
    def setPreviousVisitTime(self, value):
        self.previousVisitTime = value


    """ 
    @return DateTime
    """
    def getPreviousVisitTime(self):
        return self.previousVisitTime


    """ 
    @param DateTime value
    """
    def setCurrentVisitTime(self, value):
        self.currentVisitTime = value


    """ 
    @return DateTime
    """
    def getCurrentVisitTime(self):
        return self.currentVisitTime


    """ 
    @param int value
    """
    def setVisitlen(self, value):
        self.visitCount = value


    """ 
    @return int
    """
    def getVisitlen(self):
        return self.visitCount


    """ 
    @param string value
    """
    def setIpAddress(self, value):
        self.ipAddress = value


    """ 
    @return string
    """
    def getIpAddress(self):
        return self.ipAddress


    """ 
    @param string value
    """
    def setUserAgent(self, value):
        self.userAgent = value


    """ 
    @return string
    """
    def getUserAgent(self):
        return self.userAgent


    """ 
    @param string value
    """
    def setLocale(self, value):
        self.locale = value


    """ 
    @return string
    """
    def getLocale(self):
        return self.locale


    """ 
    @param string value
    """
    def setFlashVersion(self, value):
        self.flashVersion = value


    """ 
    @return string
    """
    def getFlashVersion(self):
        return self.flashVersion


    """ 
    @param bool value
    """
    def setJavaEnabled(self, value):
        self.javaEnabled = value


    """ 
    @return bool
    """
    def getJavaEnabled(self):
        return self.javaEnabled


    """ 
    @param int value
    """
    def setScreenColorDepth(self, value):
        self.screenColorDepth = value


    """ 
    @return string
    """
    def getScreenColorDepth(self):
        return self.screenColorDepth


    """ 
    @param string value
    """
    def setScreenResolution(self, value):
        self.screenResolution = value


    """ 
    @return string
    """
    def getScreenResolution(self):
        return self.screenResolution
