

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

from analytics import Tracker, Visitor, Session, CustomVariable
from analytics import utils, ParameterHolder, X10

class Request(HttpRequest):
    TYPE_PAGE           = None
    TYPE_EVENT          = 'event'
    TYPE_TRANSACTION    = 'tran'
    TYPE_ITEM           = 'item'
    TYPE_SOCIAL         = 'social'

    """ 
    This type of request is deprecated in favor of encoding custom variables
    within the "utme" parameter, but we include it here for completeness

    @see ParameterHolder::__utmv
    @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiBasicConfiguration.html#_gat.GA_Tracker_._setVar
    @deprecated
    @const string
    """
    TYPE_CUSTOMVARIABLE = 'var'

    X10_CUSTOMVAR_NAME_PROJECT_ID  = 8
    X10_CUSTOMVAR_VALUE_PROJECT_ID = 9
    X10_CUSTOMVAR_SCOPE_PROJECT_ID = 11

    CAMPAIGN_DELIMITER = '|'


    def __init__(self):
        self.tracker = None
        self.visitor = None
        self.session = None

    """ 
    Indicates the type of request, will be mapped to "utmt" parameter

    @see ParameterHolder::utmt
    @return string See Request::TYPE_ constants
    """
    def getType(self):
        self.x_forwarded_for = self.visitor.ip_address
        self.user_agent = self.visitor.user_agent

        # Increment session track counter for each request
        self.session.increase_tracklen()

        # See http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Configuration.as?r=237#48
        # and http://code.google.com/intl/de-DE/apis/analytics/docs/tracking/eventTrackerGuide.html#implementationConsiderations
        if self.session.tracklen > 500):
            raise Exception('Google Analytics does not guarantee to process more than 500 requests per session.')

        if self.tracker.campaign:
            self.tracker.campaign.increaseResponselen()


        return super(Request, self).build_http_request()


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def build_parameters(self):
        p = ParameterHolder()

        p.utmac = self.tracker.account_id
        p.utmhn = self.tracker.domain_name

        p.utmt = self.type
        p.utmn = utils.generate_32bit_random()

        if self.tracker.config.anonymize_ip_addresses:
            p.aip = 1
        else:
            p.aip = None

        # The IP parameter does sadly seem to be ignored by GA, so we
        # shouldn't set it as of today but keep it here for later reference
        # p.utmip = self.visitor.getIpAddress()

        p.utmhid = self.session.session_id
        p.utms   = self.session.getTracklen()

        p = self.buildVisitorParameters(p)
        p = self.buildCustomVariablesParameter(p)
        p = self.buildCampaignParameters(p)
        p = self.buildCookieParameters(p)

        return p


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder p
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def build_visitor_parameters(self, p):
        # Ensure correct locale format, see https:#developer.mozilla.org/en/navigator.language
        p.utmul = self.visitor.getLocale().replace('_', '-').lower()

        if self.visitor.getFlashVersion():
            p.utmfl = self.visitor.getFlashVersion()

        if self.visitor.getJavaEnabled():
            p.utmje = self.visitor.getJavaEnabled()

        if self.visitor.getScreenColorDepth():
            p.utmsc = self.visitor.getScreenColorDepth() + '-bit'

        p.utmsr = self.visitor.getScreenResolution()

        return p


    """ 
    @link http://xahlee.org/js/google_analytics_tracker_2010-07-01_expanded.js line 575
    @param \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder p
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def build_custom_variables_parameter(self, p):
        customVars = self.tracker.custom_variables
        if customVars:
            if len(customVars) > 5:
                # See http://code.google.com/intl/de-DE/apis/analytics/docs/tracking/gaTrackingCustomVariables.html#usage
                raise Exception('The sum of all custom variables cannot exceed 5 in any given request.')           
            
            x10 = X10()
            
            x10.clear_key(Request.X10_CUSTOMVAR_NAME_PROJECT_ID)
            x10.clear_key(Request.X10_CUSTOMVAR_VALUE_PROJECT_ID)
            x10.clear_key(Request.X10_CUSTOMVAR_SCOPE_PROJECT_ID)
            
            for custom_var in custom_vars:
                # Name and value get encoded here,
                # see http://xahlee.org/js/google_analytics_tracker_2010-07-01_expanded.js line 563
                name  = utils.encode_uri_component(custom_var.name)
                value = utils.encode_uri_component(custom_var.value)
                
                x10.set_key(Request.X10_CUSTOMVAR_NAME_PROJECT_ID, custom_var.index, name)
                x10.set_key(Request.X10_CUSTOMVAR_VALUE_PROJECT_ID, custom_var.index, value)
                if custom_var.scope is not None and custom_var.scope != CustomVariable.SCOPE_PAGE:
                    x10.set_key(Request.X10_CUSTOMVAR_SCOPE_PROJECT_ID, custom_var.index, custom_var.scope)
                
            p.utme += x10.render_url_string()

        return p


    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/GIFRequest.as#123
    @param \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder p
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def build_cookie_parameters(self, p):
        domain_hash = self.generate_domain_hash()

        p.__utma  = domain_hash + '.'
        p.__utma += self.visitor.unique_id  '.'
        p.__utma += utils.totimestamp(self.visitor.first_visit_time) + '.'
        p.__utma += utils.totimestamp(self.visitor.previous_visit_time) + '.'
        p.__utma += utils.totimestamp(self.visitor.current_visit_time) + '.'
        p.__utma += utils.totimestamp(self.visitor.visit_count)

        p.__utmb  = domain_hash + '.'
        p.__utmb += self.session.tracklen + '.'
        # FIXME: What does "token" mean? I only encountered a value of 10 in my tests.
        p.__utmb += '10.'
        p.__utmb += utils.totimestamp(self.session.start_time

        p.__utmc = domain_hash

        cookies = {}
        cookies.append('__utma=%s;' % p.__utma)
        if p.__utmz:
            cookies.append('__utmz=%s;' % p.__utmz)

        if p.__utmv:
            cookies.apend('__utmv=%s;' % p.__utmv)


        p.utmcc = '+'.join(cookies)

        return p



    """ 
    @param \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder p
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildCampaignParameters(self, p):
        campaign = self.tracker.getCampaign()
        if campaign:
            p.__utmz  = self.generateDomainHash() + '.'
            p.__utmz .= utils.totimestamp(campaign.getCreationTime()) + '.'
            p.__utmz .= self.visitor.visit_count + '.'
            p.__utmz .= campaign.getResponselen() + '.'
            
            # See http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/campaign/CampaignTracker.as#236
            data = {
                'utmcid': campaign.id,
                'utmcsr': campaign.source,
                'utmgclid': campaign.g_click_id,
                'utmdclid': campaign.d_click_id,
                'utmccn': campaign.name,
                'utmcmd': campaign.medium,
                'utmctr': campaign.term,
                'utmcct': campaign.content,
            }

            for key, value in data:
                if value:
                    # Only spaces and pluses get escaped in gaforflash and ga.js, so we do the same
                    p.__utmz += key + '=' + utils.replace_all(value, {'+': '%20', ' ': '%20'}) + Request.CAMPAIGN_DELIMITER
 
            p.__utmz = p.__utmz.rstrip(Request.CAMPAIGN_DELIMITER)

        return p


    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Tracker.as#585
    @return string
    """
    def generateDomainHash(self):
        hash = 1

        if self.tracker.allow_hash:
            hash = utils.generate_hash(self.tracker.getDomainName())

        return hash


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Tracker
    """
    def getTracker(self):
        return self.tracker


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Tracker tracker
    """
    def setTracker(self, tracker):
        self.tracker = tracker


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Visitor
    """
    def getVisitor(self):
        return self.visitor


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Visitor visitor
    """
    def setVisitor(self, visitor):
        self.visitor = visitor


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Session
    """
    def getSession(self):
        return self.session


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Session session
    """
    def setSession(self, session):
        self.session = session


