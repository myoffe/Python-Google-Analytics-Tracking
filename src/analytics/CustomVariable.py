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

from analytics.internals import utils
""" 
@link http://code.google.com/apis/analytics/docs/tracking/gaTrackingCustomVariables.html
"""
class CustomVariable(object):

    class ValidationError(Exception):
        pass



    """ 
    WATCH OUT: It's a known issue that GA will not decode URL-encoded characters
    in custom variable names and values properly, so spaces will show up
    as "%20" in the interface etc.

    @link http://www.google.com/support/forum/p/Google%20Analytics/thread?tid=2cdb3ec0be32e078
    @var mixed
    """

    """ 
    See SCOPE_ constants

    @var int
    """


    """ 
    @const int
    """
    SCOPE_VISITOR = 1
    """ 
    @const int
    """
    SCOPE_SESSION = 2
    """ 
    @const int
    """
    SCOPE_PAGE    = 3


    SCOPES = [SCOPE_VISITOR, SCOPE_SESSION, SCOPE_PAGE]


    def __init__(self, index=None, name=None, value=None, scope=None):
        self.index = index

        # WATCH OUT: It's a known issue that GA will not decode URL-encoded characters
        # in custom variable names and values properly, so spaces will show up
        # as "%20" in the interface etc.
        # http://www.google.com/support/forum/p/Google%20Analytics/thread?tid=2cdb3ec0be32e078
        self.name = name
        self.value = value
                          
        self.scope = scope or CustomVariable.SCOPE_PAGE


    def validate(self):
        """
        According to the GA documentation, there is a limit to the combined size of
        name and value of 64 bytes after URL encoding,
        see http://code.google.com/apis/analytics/docs/tracking/gaTrackingCustomVariables.html#varTypes
        and http://xahlee.org/js/google_analytics_tracker_2010-07-01_expanded.js line 563
        """

        if len( utils.encodeUriComponent(self.name + self.value) ) > 64:
            raise CustomVariable.ValidationError('Custom Variable combined name and value encoded length must not be larger than 64 bytes.')
      
    

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        """
        Custom Variables are limited to five slots officially, but there seems to be a
        trick to allow for more of them which we could investigate at a later time (see
        http://analyticsimpact.com/2010/05/24/get-more-than-5-custom-variables-in-google-analytics/)
        """
        if not 1 <= index <= 5:
            raise ValueError('Custom Variable index has to be between 1 and 5.')

        self.index = index 

    
    @property
    def scope(self):
        return self._scope


    @scope.setter
    def scope(self, scope):
        if scope not in CustomVariable.SCOPES:
            raise ValueError('Custom Variable scope has to be one of the CustomVariable.SCOPE_ constant values.')

        self.scope = scope

