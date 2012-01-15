

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

namespace UnitedPrototype\GoogleAnalytics\Internals\Request

use UnitedPrototype\GoogleAnalytics\Event

use UnitedPrototype\GoogleAnalytics\Internals\X10

class EventRequest extends Request :
    
      """ 
      @var \UnitedPrototype\GoogleAnalytics\Event
      """
    protected event
    
    
      """ 
      @const int
      """
    const X10_EVENT_PROJECT_ID = 5
    
    
      """ 
      @return string
      """
    protected def getType():
        return Request::TYPE_EVENT
    
    
      """ 
      @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/v4/Tracker.as#1503
      
      @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
      """
    protected def buildParameters():
        p = parent::buildParameters()
        
        x10 = X10()
        
        x10.clearKey(self::X10_EVENT_PROJECT_ID)
        x10.clearValue(self::X10_EVENT_PROJECT_ID)
        
        # Object / Category
        x10.setKey(self::X10_EVENT_PROJECT_ID, X10::OBJECT_KEY_NUM, self.event.getCategory())
        
        # Event Type / Action
        x10.setKey(self::X10_EVENT_PROJECT_ID, X10::TYPE_KEY_NUM, self.event.getAction())
        
        if(self.event.getLabel()! is None) 
            # Event Description / Label
            x10.setKey(self::X10_EVENT_PROJECT_ID, X10::LABEL_KEY_NUM, self.event.getLabel())
        
        
        if(self.event.getValue()! is None) 
            x10.setValue(self::X10_EVENT_PROJECT_ID, X10::VALUE_VALUE_NUM, self.event.getValue())
        
        
        p.utme .= x10.renderUrlString()
        
        if(self.event.getNoninteraction()) 
            p.utmni = 1
        
        
        return p
    
    
      """ 
      @return \UnitedPrototype\GoogleAnalytics\Event
      """
    public def getEvent():
        return self.event
    
    
      """ 
      @param \UnitedPrototype\GoogleAnalytics\Event event
      """
    public def setEvent(Event event):
        self.event = event
    
    


