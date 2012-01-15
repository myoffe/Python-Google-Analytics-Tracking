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

from googleanalyics.internals import utils
from datetime import datetime

""" 
You should serialize this object and store it in the user session to keep it
persistent between requests (similar to the "__umtb" cookie of
the GA Javascript client).
"""
class Session(object):

    """ 
    A unique per-session ID, will be mapped to "utmhid" parameter

    @see Internals\ParameterHolder::utmhid
    @var int
    """

    """ 
    The amount of pageviews that were tracked within this session so far,
    will be part of the "__utmb" cookie parameter.

    Will get incremented automatically upon each request.

    @see Internals\ParameterHolder::__utmb
    @see Internals\Request\Request::buildHttpRequest()
    @var int
    """

    """ 
    Timestamp of the start of this session, will be part of the "__utmb"
    cookie parameter

    @see Internals\ParameterHolder::__utmb
    @var DateTime
    """


    def __init__(self):
        self.sessionId = None
        self.trackCount = None
        self.startTime = None
        self.setSessionId(self.generateSessionId())
        self.setTracklen(0)
        self.setStartTime(datetime.now())
    
    
    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/DocumentInfo.as#52
    @return int
    """
    def generateSessionId(self):
        # TODO: Integrate AdSense support
        return utils.generate32bitRandom()
    
    
    """ 
    @return int
    """
    def getSessionId(self):
        return self.sessionId
    
    
    """ 
    @param int sessionId
    """
    def setSessionId(self, sessionId):
        self.sessionId = sessionId
    
    
    """ 
    @return int
    """
    def getTracklen(self):
        return self.trackCount
    
    
    """ 
    @param int trackCount
    """
    def setTracklen(self, trackCount):
        self.trackCount = trackCount
    
    
    """ 
    @param int byAmount
    """
    def increaseTracklen(self, byAmount=1):
        self.trackCount += byAmount
    

    def increase_tracklen(self, by_amount=1):
        self.track_count += by_amount

    """ 
    @return DateTime
    """
    def getStartTime(self):
        return self.startTime
    
    
    """ 
    @param DateTime startTime
    """
    def setStartTime(self, startTime):
        self.startTime = startTime
    

