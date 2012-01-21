

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

from analytics.internals.request.PageviewRequest import PageviewRequest
from analytics.internals.request.EventRequest import EventRequest
from analytics.internals.request.TransactionRequest import TransactionRequest
from analytics.internals.request.ItemRequest import ItemRequest
from analytics.internals.request.SocialInteractionRequest import SocialInteractionRequest


class AnalyticsError(Exception):
    pass


class Tracker(object):
    """
    @ivar account_id:
        Google Analytics account ID, e.g. "UA-1234567-8", will be mapped to "utmac" parameter

    @ivar domain_name:
        Host Name, e.g. "www.example.com", will be mapped to "utmhn" parameter
    
    @ivar allow_hash:
        Whether to generate a unique domain hash, default is true to be consistent
        with the GA Javascript Client

    @ivar custom_variables:
        dict of CustomVariable
        
    @ivar campaign:
        Campaign
    """

    VERSION = '5.2.2' # As of 15.11.2011
    """ 
    Google Analytics client version on which this library is built upon,
    will be mapped to "utmwv" parameter.

    This doesn't necessarily mean that all features of the corresponding
    ga.js version are implemented but rather that the requests comply
    with these of ga.js.
      
    @link http://code.google.com/apis/analytics/docs/gaJS/changelog.html
    """

    config = None
    """
    @type analytics.Config
    """


    def __init__(self, account_id, domain_name, config=None):
        Tracker.config = config

        self.allow_hash = True
        self.custom_variables = {}
        self.campaign = None
        
        self.account_id = account_id
        self.domain_name = domain_name


    RE_VALID_GA_ACCOUNT_ID = re.compile(r'UA-[0-9]-[0-9]')

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        if not Tracker.RE_VALID_GA_ACCOUNT_ID.match(value):
            raise ValueError('%s is not a valid Google Analytics account ID.' % value)

        self._account_id = value


    @property
    def domain_name(self):
        return self._domain_name

    @domain_name.setter
    def domain_name(self, value):
        self._domain_name = value


    @property
    def allow_hash(self):
        return self._allow_hash

    @allow_hash.setter
    def allow_hash(self, value):
        self._allow_hash = value


    def add_custom_variable(self, custom_variable):
        """
        Equivalent of _setCustomVar() in GA Javascript client.

        @link http://code.google.com/apis/analytics/docs/tracking/gaTrackingCustomVariables.html
        """
        # Ensure that all required parameters are set
        custom_variable.validate()
        
        index = custom_variable.index
        self.custom_variables[index] = custom_variable


    @property
    def custom_variables(self):
        return self._custom_variables


    def remove_custom_variable(self, index):
        """
        Equivalent of _deleteCustomVar() in GA Javascript client.
        """
        del self.custom_variables[index]


    @property
    def campaign(self):
        return self._campaign

    @campaign.setter
    def campaign(self, campaign = None):
        """
        Isn't really optional, but can be set to None
        """
        if campaign:
            # Ensure that all required parameters are set
            campaign.validate()
        
        self._campaign = campaign


    def track_pageview(self, page, session, visitor):
        """
        Equivalent of _trackPageview() in GA Javascript client.

        @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiBasicConfiguration.html#_gat.GA_Tracker_._trackPageview
        """
        request = PageviewRequest(Tracker.config)
        request.page = page
        request.session = session
        request.visitor = visitor
        request.tracker = self
        request.fire()


    def track_event(self, event, session, visitor):
        """
        Equivalent of _trackEvent() in GA Javascript client.

        @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEventTracking.html#_gat.GA_EventTracker_._trackEvent
        """
        # Ensure that all required parameters are set
        event.validate()
        
        request = EventRequest(Tracker.config)
        request.event = event
        request.session = session
        request.visitor = visitor
        request.tracker = self
        request.fire()


    def track_transaction(self, transaction, session, visitor):
        """
        Combines _addTrans(), _addItem() (indirectly) and _trackTrans() of GA Javascript client.
        Although the naming of "_addTrans()" would suggest multiple possible transactions
        per request, there is just one allowed actually.

        @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._addTrans
        @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._addItem
        @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._trackTrans
        """
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
      Equivalent of _track_social() in GA Javascript client.
      
    @link http://code.google.com/apis/analytics/docs/tracking/gaTrackingSocial.html#settingUp
    """
    def track_social(self, social_interaction, page, session, visitor):
        request = SocialInteractionRequest(Tracker.config)
        request.social_interaction = social_interaction
        request.page = page
        request.session = session
        request.visitor = visitor
        request.tracker = self
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
        from analytics.Config import Config

        if cls.config:
            errorSeverity = cls.config.getErrorSeverity()
        else:
            errorSeverity = Config.ERROR_SEVERITY_EXCEPTIONS
        
        if errorSeverity == Config.ERROR_SEVERITY_SILENCE:
            pass
        elif errorSeverity == Config.ERROR_SEVERITY_WARNINGS:
            logger.warning(message)
        elif errorSeverity == Config.ERROR_SEVERITY_EXCEPTIONS:
            raise AnalyticsError(message)

