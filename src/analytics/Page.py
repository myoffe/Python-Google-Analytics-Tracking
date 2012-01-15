

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

class Page(object):
    
    """ 
    Page request URI, e.g. "/path/page.html", will be mapped to
    "utmp" parameter

    @see Internals\ParameterHolder::utmp
    @var string
    """

    """ 
    Page title, will be mapped to "utmdt" parameter

    @see Internals\ParameterHolder::utmdt
    @var string
    """

    """ 
    Charset encoding (e.g. "UTF-8"), will be mapped to "utmcs" parameter

    @see Internals\ParameterHolder::utmcs
    @var string
    """

    """ 
    Referer URL, e.g. "http://www.example.com/path/page.html",  will be
    mapped to "utmr" parameter

    @see Internals\ParameterHolder::utmr
    @var string
    """

    """ 
    Page load time in milliseconds, will be encoded into "utme" parameter.

    @see Internals\ParameterHolder::utme
    @var int
    """
    """ 
    Constant to mark referrer as a site-internal one.

    @see Page::referrer
    @const string
    """
    REFERRER_INTERNAL = '0'
    
    
    """ 
    @param string path
    """
    def __init__(self, path):
        self.title = None
        self.charset = None
        self.referrer = None
        self.loadTime = None
        self.path = None

        self.setPath(path)
    
    
    """ 
    @param string path
    """
    def setPath(self, path):
        if path and path[0] != '/':
            raise ValueError('The page path should always start with a slash ("/").')
        
        self.path = path
    
    
    """ 
    @return string
    """
    def getPath(self):
        return self.path
    
    
    """ 
    @param string title
    """
    def setTitle(self, title):
        self.title = title
    
    
    """ 
    @return string
    """
    def getTitle(self):
        return self.title
    
    
    """ 
    @param string charset
    """
    def setCharset(self, encoding):
        self.charset = encoding
    
    
    """ 
    @return string
    """
    def getCharset(self):
        return self.charset
    
    
    """ 
    @param string referrer
    """
    def setReferrer(self, referrer):
        self.referrer = referrer
    
    
    """ 
    @return string
    """
    def getReferrer(self):
        return self.referrer
    
    
    """ 
    @param int loadTime
    """
    def setLoadTime(self, loadTime):
        if not isinstance(loadTime, int):
            raise ValueError('Page load time must be specified in integer milliseconds.')
        
        self.loadTime = loadTime
    
    
    """ 
    @return int
    """
    def getLoadTime(self):
        return self.loadTime
    
    


