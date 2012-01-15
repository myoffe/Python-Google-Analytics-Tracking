

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

from analytics.internals import Request


class ItemRequest(Request):

    def __init__(self):
        self.item = None


    """ 
    @return string
    """
    def getType(self):
        return Request.TYPE_ITEM


    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/ecommerce/Item.as#61

    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildParameters(self):
        p = super(ItemRequest, self).buildParameters()        

        p.utmtid = self.item.getOrderId()
        p.utmipc = self.item.getSku()
        p.utmipn = self.item.getName()
        p.utmiva = self.item.getVariation()
        p.utmipr = self.item.getPrice()
        p.utmiqt = self.item.getQuantity()  

        return p


    """ 
    The GA Javascript client doesn't send any visitor information for
    e-commerce requests, so we don't either.

    @param \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder p
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildVisitorParameters(self, p):
        return p


    """ 
    The GA Javascript client doesn't send any custom variables for
    e-commerce requests, so we don't either.

    @param \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder p
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildCustomVariablesParameter(self, p):
        return p


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Item
    """
    def getItem(self):
        return self.item


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Item item
    """
    def setItem(self, item):
        self.item = item




