

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

from analytics.internals.requests import Request


use UnitedPrototype\GoogleAnalytics\Transaction
use UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder

class TransactionRequest(Request):

    def __init__(self):
    self.transaction = None

    """ 
    @return string
    """
    def getType(self):
        return Request.TYPE_TRANSACTION


    """ 
    @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/ecommerce/Transaction.as#76

    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildParameters(self):
        p = super(TransactionRequest, self).buildParameters()

        p.utmtid = self.transaction.getOrderId()
        p.utmtst = self.transaction.getAffiliation()
        p.utmtto = self.transaction.getTotal()
        p.utmttx = self.transaction.getTax()
        p.utmtsp = self.transaction.getShipping()
        p.utmtci = self.transaction.getCity()
        p.utmtrg = self.transaction.getRegion()
        p.utmtco = self.transaction.getCountry()

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
    @return \UnitedPrototype\GoogleAnalytics\Transaction
    """
    def getTransaction():
        return self.transaction


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Transaction transaction
    """
    def setTransaction(self, transaction):
        self.transaction = transaction




