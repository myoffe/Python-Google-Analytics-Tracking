

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

from analytics.internal.request import Request, PageviewRequest

class SocialinteractionRequest(PageviewRequest):

    """ 
    @var \UnitedPrototype\GoogleAnalytics\SocialInteraction
    """
    
    def __init__(self):
        self.socialInteraction = None


    """ 
    @return string
    """
    def getType(self):
        return Request.TYPE_SOCIAL


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildParameters(self):
        p = super(SocialinteractionRequest, self).buildParameters()

        p.utmsn  = self.socialInteraction.getNetwork()
        p.utmsa  = self.socialInteraction.getAction()
        p.utmsid = self.socialInteraction.getTarget()
        if not p.utmsid:
            # Default to page path like ga.js,
            # see http://code.google.com/apis/analytics/docs/tracking/gaTrackingSocial.html#settingUp
            p.utmsid = self.page.getPath()

        return p


    """ 
    @return \UnitedPrototype\GoogleAnalytics\SocialInteraction
    """
    def getSocialInteraction(self):
        return self.socialInteraction


    """ 
    @param \UnitedPrototype\GoogleAnalytics\SocialInteraction socialInteraction
    """
    def setSocialInteraction(self, socialInteraction):
        self.socialInteraction = socialInteraction




