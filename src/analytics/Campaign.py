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
from urlparse import urlparse


""" 
You should serialize this object and store it in e.g. the user database to keep it
persistent for the same user permanently (similar to the "__umtz" cookie of
the GA Javascript client).
"""
class Campaign(object):
    
    class ValidationError(Exception):
        pass

    """ 
    See self::TYPE_ constants, will be mapped to "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    type
    """
    
    """ 
    Time of the creation of this campaign, will be mapped to "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var DateTime

    creationTime
    """

    """ 
    Response Count, will be mapped to "__utmz" parameter.

    Is also used to determine whether the campaign is or repeated,
    which will be mapped to "utmcn" and "utmcr" parameters.

    @see Internals\ParameterHolder::__utmz
    @see Internals\ParameterHolder::utmcn
    @see Internals\ParameterHolder::utmcr
    @var int

    responseCount = 0
    """

    """ 
    Campaign ID, a.k.a. "utm_id" query parameter for ga.js
    Will be mapped to "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var int

    id
    """

    """ 
    Source, a.k.a. "utm_source" query parameter for ga.js.
    Will be mapped to "utmcsr" key in "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    source
    """

    """ 
    Google AdWords Click ID, a.k.a. "gclid" query parameter for ga.js.
    Will be mapped to "utmgclid" key in "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    gClickId
    """

    """ 
    DoubleClick (?) Click ID. Will be mapped to "utmdclid" key in "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    dClickId
    """

    """ 
    Name, a.k.a. "utm_campaign" query parameter for ga.js.
    Will be mapped to "utmccn" key in "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    name
    """

    """ 
    Medium, a.k.a. "utm_medium" query parameter for ga.js.
    Will be mapped to "utmcmd" key in "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    medium
    """

    """ 
    Terms/Keywords, a.k.a. "utm_term" query parameter for ga.js.
    Will be mapped to "utmctr" key in "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    term
    """

    """ 
    Ad Content Description, a.k.a. "utm_content" query parameter for ga.js.
    Will be mapped to "utmcct" key in "__utmz" parameter.

    @see Internals\ParameterHolder::__utmz
    @var string

    content
    """
        
    TYPE_DIRECT = 'direct'
    TYPE_ORGANIC = 'organic'
    TYPE_REFERRAL = 'referral'
    TYPES = [TYPE_DIRECT, TYPE_ORGANIC, TYPE_REFERRAL]

    """ 
    @see createFromReferrer
    @param string type See TYPE_ constants
    """
    def __init__(self, type_):
        self.responseCount = 0
        if type_ not in Campaign.TYPES:
            raise ValueError('Campaign type has to be one of the Campaign::TYPE_ constant values.')
        
        
        self.type = type_
        
        if type_ == Campaign.TYPE_DIRECT:
            # See http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/campaign/CampaignManager.as#375
            self.name   = '(direct)'
            self.source = '(direct)'
            self.medium = '(none)'
        elif type_ == Campaign.TYPE_REFERRAL:
            # See http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/campaign/CampaignManager.as#340
            self.name   = '(referral)'
            self.medium = 'referral'
        elif type_ == Campaign.TYPE_ORGANIC:
            # See http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/campaign/CampaignManager.as#280
            self.name   = '(organic)'
            self.medium = 'organic'
        
        self.creationTime = datetime.datetime.now()
    
    
    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/campaign/CampaignManager.as#333
    @param string url
    @return \UnitedPrototype\GoogleAnalytics\Campaign
    """
    @classmethod
    def createFromReferrer(cls, url):
        instance = cls(Campaign.TYPE_REFERRAL)
        urlInfo = urlparse(url)
        instance.source  = urlInfo.hostname
        instance.content = urlInfo.path
        
        return instance
    
    
    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/campaign/CampaignTracker.as#153
    """
    def validate(self):
        # NOTE: gaforflash states that id and gClickId must also be specified,
        # but that doesn't seem to be correct
        if not self.source:
            raise Campaign.ValidationError('Campaigns need to have at least the "source" attribute defined.')
        
    
    
    """ 
    @param string type
    """
    def setType(self, type_):
        self.type = type_
    
    
    """ 
    @return string
    """
    def getType(self):
        return self.type
    
    
    """ 
    @param DateTime creationTime
    """
    def setCreationTime(self, creationTime):
        self.creationTime = creationTime
    
    
    """ 
    @return DateTime
    """
    def getCreationTime(self):
        return self.creationTime
    

    """ 
    @param int esponseCount
    """
    def setResponselen(self, responseCount):
        self.responseCount = responseCount
    
    
    """ 
    @return int
    """
    def getResponselen(self):
        return self.responseCount
    
    
    """ 
    @param int byAmount
    """
    def increaseResponselen(self, byAmount = 1):
        self.responseCount += byAmount
    

    """ 
    @param int id
    """
    def setId(self, id_):
        self.id = id_
    
    
    """ 
    @return int
    """
    def getId(self):
        return self.id
    
    
    """ 
    @param string source
    """
    def setSource(self, source):
        self.source = source
    
    
    """ 
    @return string
    """
    def getSource(self):
        return self.source
    
    
    """ 
    @param string gClickId
    """
    def setGClickId(self, gClickId):
        self.gClickId = gClickId
    
    
    """ 
    @return string
    """
    def getGClickId(self):
        return self.gClickId
    
    
    """ 
    @param string dClickId
    """
    def setDClickId(self, dClickId):
        self.dClickId = dClickId
    
    
    """ 
    @return string
    """
    def getDClickId(self):
        return self.dClickId


    """ 
    @param string name
    """
    def setName(self, name):
        self.name = name


    """ 
    @return string
    """
    def getName(self):
        return self.name


    """ 
    @param string medium
    """
    def setMedium(self, medium):
        self.medium = medium


    """ 
    @return string
    """
    def getMedium(self):
        return self.medium


    """ 
    @param string term
    """
    def setTerm(self, term):
        self.term = term


    """ 
    @return string
    """
    def getTerm(self):
        return self.term


    """ 
    @param string content
    """
    def setContent(self, content):
        self.content = content


    """ 
    @return string
    """
    def getContent(self):
        return self.content

