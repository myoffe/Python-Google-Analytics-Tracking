

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

class Transaction(object):
    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/ecommerce/Transaction.as


    @ivar order_id:
        Order ID, e.g. "a2343898", will be mapped to "utmtid" parameter
    
    @ivar affiliation:
        Affiliation, Will be mapped to "utmtst" parameter

    @ivar total:
        Total Cost, will be mapped to "utmtto" parameter

    @ivar tax:
        Tax Cost, will be mapped to "utmttx" parameter

    @ivar shipping:
        Shipping Cost, values as for unit and price, e.g. 3.95, will be mapped to
        "utmtsp" parameter

    @ivar city:
        Billing City, e.g. "Cologne", will be mapped to "utmtci" parameter

    @ivar region:
        Billing Region, e.g. "North Rhine-Westphalia", will be mapped to "utmtrg" parameter

    @ivar country:
        Billing Country, e.g. "Germany", will be mapped to "utmtco" parameter

    @ivar items:
        Dictionary of Items
    """
    
    class ValidationError(Exception):
        pass


    def __init__(self):
        self.orderId = None
        self.affiliation = None
        self.total = None
        self.tax = None
        self.shipping = None
        self.city = None
        self.region = None
        self.country = None
        self._items = {}

    
    
    def validate(self):
        if not self.items:
            raise Transaction.ValidationError('Transactions need to consist of at least one item.')
        
    
    
    def add_item(self, item):
        """ 
        @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEcommerce.html#_gat.GA_Tracker_._addItem
        """
        # Associated items inherit the transaction's order ID
        item.oder_id = self.order_id
        
        self.items[item.sku] = item
    
    
    def items(self):
        return self._items
    
    
    @property
    def order_id(self):
        return self.orderId
    
    
    @order_id.setter
    def order_id(self, order_id):
        self.order_id = order_id
        
        # Update order IDs of all associated items too
        for item in self.items:
            item.set_order_id(order_id)
        
