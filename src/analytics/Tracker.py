

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

import re

from googleanalytics.internals.request.PageviewRequest import PageviewRequest
from googleanalytics.internals.request.EventRequest import EventRequest
from googleanalytics.internals.request.TransactionRequest import TransactionRequest
from googleanalytics.internals.request.ItemRequest import ItemRequest
from googleanalytics.internals.request.SocialInteractionRequest import SocialInteractionRequest


class Tracker(object):

    """ 
      Google Analytics client version on which this library is built upon,
      will be mapped to "utmwv" parameter.
      
      This doesn't necessarily mean that all features of the corresponding
      ga.js version are implemented but rather that the requests comply
      with these of ga.js.
      
    @link http://code.google.com/apis/analytics/docs/gaJS/changelog.html
    @const string
    """
    VERSION = '5.2.2' # As of 15.11.2011


    """ 
      The configuration to use for all tracker instances.
      
    @var \UnitedPrototype\GoogleAnalytics\Config
    """
    config = None

    """ 
      Google Analytics account ID, e.g. "UA-1234567-8", will be mapped to
    "utmac" parameter
      
    @see Internals\ParameterHolder::utmac
    @var string
    """

    """ 
      Host Name, e.g. "www.example.com", will be mapped to "utmhn" parameter
      
    @see Internals\ParameterHolder::utmhn
    @var string
    """

    """ 
      Whether to generate a unique domain hash, default is True to be consistent
      with the GA Javascript Client
      
    @link http://code.google.com/apis/analytics/docs/tracking/gaTrackingSite.html#setAllowHash
    @see Internals\Request\Request::generateDomainHash()
    @var bool
    """

    """ 
    @var array
    """

    """ 
    @var \UnitedPrototype\GoogleAnalytics\Campaign
    """


    """ 
    @param string accountId
    @param string domainName
    @param \UnitedPrototype\GoogleAnalytics\Config config
    """
    def __init__(self, accountId, domainName, config=None):
        Tracker.config = config

        self.allowHash = True
        self.customVariables = {}
        self.campaign = None
        
        self.setAccountId(accountId)
        self.setDomainName(domainName)


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Config
    """
    @classmethod
    def getConfig(cls):
        return cls.config
        

    """ 
    @param \UnitedPrototype\GoogleAnalytics\Config value
    """
    @classmethod    
    def setConfig(cls, value):
        cls.config = value


    """ 
    @param string value
    """
    RE_VALID_GA_ACCOUNT_ID = re.compile(r'UA-[0-9]-[0-9]')
    def setAccountId(self, value):
        if not Tracker.RE_VALID_GA_ACCOUNT_ID.match(value):
            raise ValueError('%s is not a valid Google Analytics account ID.' % value)
        
        self.accountId = value


    """ 
    @return string
    """
    def getAccountId(self):
        return self.accountId


    """ 
    @param string value
    """
    def setDomainName(self, value):
        self.domainName = value


    """ 
    @return string
    """
    def getDomainName(self):
        return self.domainName


    """ 
    @param bool value
    """
    def setAllowHash(self, value):
        self.allowHash = value


    """ 
    @return bool
    """
    def getAllowHash(self):
        return self.allowHash


    """ 
      Equivalent of _setCustomVar() in GA Javascript client.
      
    @link http://code.google.com/apis/analytics/docs/tracking/gaTrackingCustomVariables.html
    @param \UnitedPrototype\GoogleAnalytics\CustomVariable customVariable
    """
    def addCustomVariable(self, customVariable):
        # Ensure that all required parameters are set
        customVariable.validate()
        
        index = customVariable.getIndex()
        self.customVariables[index] = customVariable


    """ 
    @return \UnitedPrototype\GoogleAnalytics\CustomVariable[]
    """
    def getCustomVariables(self):
        return self.customVariables


    """ 
      Equivalent of _deleteCustomVar() in GA Javascript client.
      
    @param int index
    """
    def removeCustomVariable(self, index):
        del self.customVariables[index]


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Campaign campaign Isn't really optional, but can be set to None
    """
    def setCampaign(self, campaign = None):
        if campaign:
            # Ensure that all required parameters are set
            campaign.validate()
        
        self.campaign = campaign


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Campaign|None
    """
    def getCampaign(self):
        return self.campaign


    """ 
      Equivalent of _trackPageview() in GA Javascript client.
      
    @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiBasicConfiguration.html#_gat.GA_Tracker_._trackPageview
    @param \UnitedPrototype\GoogleAnalytics\Page page
    @param \UnitedPrototype\GoogleAnalytics\Session session
    @param \UnitedPrototype\GoogleAnalytics\Visitor visitor
    """
    def trackPageview(self, page, session, visitor):
        request = PageviewRequest(Tracker.config)
        request.setPage(page)
        request.setSession(session)
        request.setVisitor(visitor)
        request.setTracker(self)
        request.fire()


    """ 
      Equivalent of _trackEvent() in GA Javascript client.
      
    @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEventTracking.html#_gat.GA_EventTracker_._trackEvent
    @param \UnitedPrototype\GoogleAnalytics\Event event
    @param \UnitedPrototype\GoogleAnalytics\Session session
    @param \UnitedPrototype\GoogleAnalytics\Visitor visitor
    """
    def trackEvent(self, event, session, visitor):
        # Ensure that all required parameters are set
        event.validate()
        
        request = EventRequest(Tracker.config)
        request.setEvent(event)
        request.setSession(session)
        request.setVisitor(visitor)
        request.setTracker(self)
        request.fire()


    """ 
      Combines _addTrans(), _addItem() (indirectly) and _trackTrans() of GA Javascript client.
      Although the naming of "_addTrans()" would suggest multiple possible transactions
      per request, there is just one allowed actually.
      
    @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._addTrans
    @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._addItem
    @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._trackTrans
      
    @param \UnitedPrototype\GoogleAnalytics\Transaction transaction
    @param \UnitedPrototype\GoogleAnalytics\Session session
    @param \UnitedPrototype\GoogleAnalytics\Visitor visitor
    """
    def trackTransaction(self, transaction, session, visitor):
        # Ensure that all required parameters are set
        transaction.validate()
        
        request = TransactionRequest(Tracker.config)
        request.setTransaction(transaction)
        request.setSession(session)
        request.setVisitor(visitor)
        request.setTracker(self)
        request.fire()
        
        # Every item gets a separate request,
        # see http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Tracker.as#312
        for item in transaction.getItems():
            # Ensure that all required parameters are set
            item.validate()
            
            request = ItemRequest(Tracker.config)
            request.setItem(item)
            request.setSession(session)
            request.setVisitor(visitor)
            request.setTracker(self)
            request.fire()
        


    """ 
      Equivalent of _trackSocial() in GA Javascript client.
      
    @link http://code.google.com/apis/analytics/docs/tracking/gaTrackingSocial.html#settingUp
    @param \UnitedPrototype\GoogleAnalytics\SocialInteraction socialInteraction
    @param \UnitedPrototype\GoogleAnalytics\Page page
    @param \UnitedPrototype\GoogleAnalytics\Session session
    @param \UnitedPrototype\GoogleAnalytics\Visitor visitor
    """
    def trackSocial(self, socialInteraction, page, session, visitor):
        request = SocialInteractionRequest(Tracker.config)
        request.setSocialInteraction(socialInteraction)
        request.setPage(page)
        request.setSession(session)
        request.setVisitor(visitor)
        request.setTracker(self)
        request.fire()


    """ 
      For internal use only. Will trigger an error according to the current
      Config::errorSeverity setting.
      
    @see Config::errorSeverity
    @param string message
    @param string method
    """

    @classmethod
    def raiseError(cls, message, logger):
        from googleanalytics.Config import Config

        if cls.config:
            errorSeverity = cls.config.getErrorSeverity()
        else:
            errorSeverity = Config.ERROR_SEVERITY_EXCEPTIONS
        
        if errorSeverity == Config.ERROR_SEVERITY_SILENCE:
            pass
        elif errorSeverity == Config.ERROR_SEVERITY_WARNINGS:
            logger.warning(message)
        elif errorSeverity == Config.ERROR_SEVERITY_EXCEPTIONS:
            raise Exception(message)

