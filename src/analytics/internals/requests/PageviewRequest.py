

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

import math

from analytics.internals import Request, X10

class PageviewRequest(Request):

    X10_SITESPEED_PROJECT_ID = 14


    def __init__(self):
        self.page = None

    """ 
    @return string
    """
    def getType(self):
        return Request.TYPE_PAGE


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildParameters(self):
        p = super(PageviewRequest, self).buildParameters()

        p.utmp  = self.page.getPath()
        p.utmdt = self.page.getTitle()
        if self.page.getCharset():
            p.utmcs = self.page.getCharset()

        if self.page.getReferrer():
            p.utmr = self.page.getReferrer()

        if self.page.getLoadTime() is not None:
            # Sample sitespeed measurements
            if p.utmn % 100 < self.config.getSitespeedSampleRate():
                x10 = X10()
                
                x10.clearKey(PageviewRequest.X10_SITESPEED_PROJECT_ID)
                x10.clearValue(PageviewRequest.X10_SITESPEED_PROJECT_ID)
                
                # Taken from ga.js code
                key = max(min(math.floor(self.page.getLoadTime() / 100), 5000), 0) * 100
                x10.setKey(PageviewRequest.X10_SITESPEED_PROJECT_ID, X10.OBJECT_KEY_NUM, key)
                
                x10.setValue(self.X10_SITESPEED_PROJECT_ID, X10.VALUE_VALUE_NUM, self.page.getLoadTime())
                
                p.utme += x10.renderUrlString()
            
        return p


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Page
    """
    def getPage(self):
        return self.page


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Page page
    """
    def setPage(self, page):
        self.page = page




