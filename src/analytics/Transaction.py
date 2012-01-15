

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

""" 
@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/ecommerce/Transaction.as
"""
class Transaction(object):
    
    class ValidationError(Exception):
        pass
    """ 
    Order ID, e.g. "a2343898", will be mapped to "utmtid" parameter

    @see Internals\ParameterHolder::utmtid
    @var string
    """

    """ 
    Affiliation, Will be mapped to "utmtst" parameter

    @see Internals\ParameterHolder::utmtst
    @var string
    """

    """ 
    Total Cost, will be mapped to "utmtto" parameter

    @see Internals\ParameterHolder::utmtto
    @var float
    """

    """ 
    Tax Cost, will be mapped to "utmttx" parameter

    @see Internals\ParameterHolder::utmttx
    @var float
    """

    """ 
    Shipping Cost, values as for unit and price, e.g. 3.95, will be mapped to
    "utmtsp" parameter

    @see Internals\ParameterHolder::utmtsp
    @var float
    """

    """ 
    Billing City, e.g. "Cologne", will be mapped to "utmtci" parameter

    @see Internals\ParameterHolder::utmtci
    @var string
    """

    """ 
    Billing Region, e.g. "North Rhine-Westphalia", will be mapped to "utmtrg" parameter

    @see Internals\ParameterHolder::utmtrg
    @var string
    """

    """ 
    Billing Country, e.g. "Germany", will be mapped to "utmtco" parameter

    @see Internals\ParameterHolder::utmtco
    @var string
    """

    """ 
    @see Transaction::addItem()
    @var \UnitedPrototype\GoogleAnalytics\Item[]
    """

    def __init__(self):
        self.orderId = None
        self.affiliation = None
        self.total = None
        self.tax = None
        self.shipping = None
        self.city = None
        self.region = None
        self.country = None
        self.items = {}

    
    
    def validate(self):
        if not self.items:
            raise Transaction.ValidationError('Transactions need to consist of at least one item.')
        
    
    
    """ 
    @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._addItem
    @param \UnitedPrototype\GoogleAnalytics\Item item
    """
    def addItem(self, item):
        # Associated items inherit the transaction's order ID
        item.setOrderId(self.orderId)
        
        sku = item.getSku()
        self.items[sku] = item
    
    
    """ 
    @return \UnitedPrototype\GoogleAnalytics\Item[]
    """
    def getItems(self):
        return self.items
    
    
    """ 
    @return string
    """
    def getOrderId(self):
        return self.orderId
    
    
    """ 
    @param string orderId
    """
    def setOrderId(self, orderId):
        self.orderId = orderId
        
        # Update order IDs of all associated items too
        for item in self.items:
            item.setOrderId(orderId)
        
    
    
    """ 
    @return string
    """
    def getAffiliation(self):
        return self.affiliation
    
    
    """ 
    @param string affiliation
    """
    def setAffiliation(self, affiliation):
        self.affiliation = affiliation
    
    
    """ 
    @return float
    """
    def getTotal(self):
        return self.total
    
    
    """ 
    @param float total
    """
    def setTotal(self, total):
        self.total = total
    
    
    """ 
    @return float
    """
    def getTax(self):
        return self.tax
    
    
    """ 
    @param float tax
    """
    def setTax(self, tax):
        self.tax = tax
    
    
    """ 
    @return float
    """
    def getShipping(self):
        return self.shipping
    
    
    """ 
    @param float shipping
    """
    def setShipping(self, shipping):
        self.shipping = shipping
    
    
    """ 
    @return string
    """
    def getCity(self):
        return self.city
    
    
    """ 
    @param string city
    """
    def setCity(self, city):
        self.city = city
    
    
    """ 
    @return string
    """
    def getRegion(self):
        return self.region
    
    
    """ 
    @param string region
    """
    def setRegion(self, region):
        self.region = region
    
    
    """ 
    @return string
    """
    def getCountry(self):
        return self.country
    
    
    """ 
    @param string country
    """
    def setCountry(self, country):
        self.country = country
    
    


