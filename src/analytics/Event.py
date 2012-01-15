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
@link http://code.google.com/apis/analytics/docs/tracking/eventTrackerOverview.html
@link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiEventTracking.html
"""
class Event(object):
    
    class ValidationError(Exception):
        pass

    """ 
    The general event category (e.g. "Videos").

    @var string
    """

    """ 
    The action for the event (e.g. "Play").

    @var string
    """

    """ 
    An optional descriptor for the event (e.g. the video's title).

    @var string
    """

    """ 
    An optional value associated with the event. You can see your event values in the Overview,
    Categories, and Actions reports, where they are listed by event or aggregated across events,
    depending upon your report view.

    @var int
    """

    """ 
    Default value is False. By default, event hits will impact a visitor's bounce rate.
    By setting this parameter to True, this event hit will not be used in bounce rate calculations.

    @var bool
    """

    
    """ 
    @param string category
    @param string action
    @param string label
    @param int value
    @param bool noninteraction
    """
    def __init__(self, category=None, action=None, label=None, value=None, noninteraction=None):
        self.setCategory(category)
        self.setAction(action)
        self.setLabel(label)
        self.setValue(value)
        self.setNoninteraction(noninteraction)
       
    def validate(self):
        if self.category is None or self.action is None:
            Event.ValidationError('Events need at least to have a category and action defined.')
        
    

    """ 
    @return string
    """
    def getCategory(self):
        return self.category


    """ 
    @param string category
    """
    def setCategory(self, category):
        self.category = category


    """ 
    @return string
    """
    def getAction(self):
        return self.action


    """ 
    @param string action
    """
    def setAction(self, action):
        self.action = action


    """ 
    @return string
    """
    def getLabel(self):
        return self.label


    """ 
    @param string label
    """
    def setLabel(self, label):
        self.label = label


    """ 
    @return int
    """
    def getValue(self):
        return self.value


    """ 
    @param int value
    """
    def setValue(self, value):
        self.value = value


    """ 
    @return bool
    """
    def getNoninteraction(self):
      return self.noninteraction


    """ 
    @param bool value
    """
    def setNoninteraction(self, value):
        self.noninteraction = value




