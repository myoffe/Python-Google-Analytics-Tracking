

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

@link      http:#code.google.com/p/php-ga

@license   http:#www.gnu.org/licenses/lgpl.html
@author    Thomas Bachem <tb@unitedprototype.com>
@copyright Copyright (c) 2010 United Prototype GmbH (http:#unitedprototype.com)
"""


from analytics import Tracker

""" 
This simple class is mainly meant to be a well-documented overview of all
possible GA tracking parameters.

@link http:#code.google.com/apis/analytics/docs/tracking/gaTrackingTroubleshooting.html#gifParameters
"""
class AttrDict(dict):
    """
    A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.
    
    @link http://code.activestate.com/recipes/473786-dictionary-with-attribute-style-access/
    """

    """
    Override defaults in a subclass to set default values for any instance of AttrDict
    """
    defaults = {}

    def __init__(self, init={}):
        init.update(self.__class__.defaults)
        dict.__init__(self, init)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(AttrDict, self).__getitem__(name)

    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__



class ParameterHolder(AttrDict):
    defaults = {
        'utmwv': Tracker.VERSION,
        'utmcs': '-',
        'utmr': '-',
        'utmfl': '-',
        'utmje': '-',
    }
