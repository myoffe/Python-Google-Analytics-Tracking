

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
@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/ecommerce/Item.as
"""
class Item(object):

    class ValidationError(Exception):
        pass
    """ 
    Order ID, e.g. "a2343898", will be mapped to "utmtid" parameter

    @see Internals\ParameterHolder::utmtid
    @var string
    """

    """ 
    Product Code. This is the sku code for a given product, e.g. "989898ajssi",
    will be mapped to "utmipc" parameter

    @see Internals\ParameterHolder::utmipc
    @var string
    """

    """ 
    Product Name, e.g. "T-Shirt", will be mapped to "utmipn" parameter

    @see Internals\ParameterHolder::utmipn
    @var string
    """

    """ 
    Variations on an item, e.g. "white", "black", "green" etc., will be mapped
    to "utmiva" parameter

    @see Internals\ParameterHolder::utmiva
    @var string
    """

    """ 
    Unit Price. Value is set to numbers only (e.g. 19.95), will be mapped to
    "utmipr" parameter

    @see Internals\ParameterHolder::utmipr
    @var float
    """

    """ 
    Unit Quantity, e.g. 4, will be mapped to "utmiqt" parameter

    @see Internals\ParameterHolder::utmiqt
    @var int
    """
    
    def __init__(self):
        self.orderId = None
        self.sku = None
        self.name = None
        self.variation = None
        self.price = None
        self.quantity = 1

    
    def validate(self):
        if self.sku is None:
            raise Item.ValidationError('Items need to have a sku/product code defined.')
        

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
    

    """ 
    @return string
    """
    def getSku(self):
        return self.sku
    
    
    """ 
    @param string sku
    """
    def setSku(self, sku):
        self.sku = sku
    
    
    """ 
    @return string
    """
    def getName(self):
        return self.name
    
    
    """ 
    @param string name
    """
    def setName(self, name):
        self.name = name
    
    
    """ 
    @return string
    """
    def getVariation(self):
        return self.variation
    
    
    """ 
    @param string variation
    """
    def setVariation(self, variation):
        self.variation = variation
    
    
    """ 
    @return float
    """
    def getPrice(self):
        return self.price
    
    
    """ 
    @param float price
    """
    def setPrice(self, price):
        self.price = price
    
    
    """ 
    @return int
    """
    def getQuantity(self):
        return self.quantity
    
    
    """ 
    @param int quantity
    """
    def setQuantity(self, quantity):
        self.quantity = quantity
    
    