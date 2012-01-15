

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

from analytics import Config
from analytics.internals import utils


""" 
@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/GIFRequest.as
"""
class HttpRequest(object):

    def __init__(self, self, config=None):
        # Indicates the type of request, will be mapped to "utmt" parameter
        # @see ParameterHolder::utmt
        # @var string
        self.type = None

        self.config = None
        self.xForwardedFor = None
        self.userAgent = None

        self.setConfig(config or Config())
    

    """ 
    @return \UnitedPrototype\GoogleAnalytics\Config
    """
    def getConfig(self):
        return self.config


    """ 
    @param \UnitedPrototype\GoogleAnalytics\Config config
    """
    def setConfig(self, config):
        self.config = config


    """ 
    @param string value
    """
    def setXForwardedFor(self, value):
        self.xForwardedFor = value


    """ 
    @param string value
    """
    def setUserAgent(self, value):
        self.userAgent = value


    """ 
    @return string
    """
    def buildHttpRequest(self):
        parameters = self.buildParameters()

        # This constant is supported as the 4th argument of http_build_query()
        # from PHP 5.3.6 on and will tell it to use rawurlencode() instead of urlencode()
        # internally, see http://code.google.com/p/php-ga/issues/detail?id=3
        if(defined('PHP_QUERY_RFC3986')) 
            # http_build_query() does automatically skip all array entries
            # with None values, exactly what we want here
            queryString = http_build_query(parameters.toArray(), '', '&', PHP_QUERY_RFC3986)
         else:
            # Manually replace "+"s with "%20" for backwards-compatibility
            queryString = str_replace('+', '%20', http_build_query(parameters.toArray(), '', '&'))

        # Mimic Javascript's encodeURIComponent() encoding for the query
        # string just to be sure we are 100% consistent with GA's Javascript client
        queryString = Util::convertToUriComponentEncoding(queryString)

        # Recent versions of ga.js use HTTP POST requests if the query string is too long
        usePost = strlen(queryString) > 2036

        if( not usePost) 
            r = 'GET ' . self.config.getEndpointPath() . '?' . queryString . ' HTTP/1.0' . "\r\n"
         else:
            # FIXME: The "/p" shouldn't be hardcoded here, instead we need a GET and a POST endpoint...
            r = 'POST /p' . self.config.getEndpointPath() . ' HTTP/1.0' . "\r\n"

        r .= 'Host: ' . self.config.getEndpointHost() . "\r\n"

        if(self.userAgent) 
            r .= 'User-Agent: ' . str_replace(array("\n", "\r"), '', self.userAgent) . "\r\n"


        if(self.xForwardedFor) 
            # Sadly "X-Fowarded-For" is not supported by GA so far,
            # see e.g. http://www.google.com/support/forum/p/Google+Analytics/thread?tid=017691c9e71d4b24,
            # but we include it nonetheless for the pure sake of correctness (and hope)
            r .= 'X-Forwarded-For: ' . str_replace(array("\n", "\r"), '', self.xForwardedFor) . "\r\n"


        if(usePost) 
            # Don't ask me why "text/plain", but ga.js says so :)
            r .= 'Content-Type: text/plain' . "\r\n"
            r .= 'Content-Length: ' . strlen(queryString) . "\r\n"


        r .= 'Connection: close' . "\r\n"
        r .= "\r\n\r\n"

        if(usePost) 
            r .= queryString


        return r


    """ 
    @return \UnitedPrototype\GoogleAnalytics\Internals\ParameterHolder
    """
    def buildParameters(self):
        request = self.buildHttpRequest()
        response = None

        # Do not actually send the request if endpoint host is set to None
        if self.config.getEndpointHost():
            timeout = self.config.getRequestTimeout()
            
            socket = fsockopen(self.config.getEndpointHost(), 80, errno, errstr, timeout)
            if( not socket) return False
            
            if(self.config.getFireAndForget()) 
                stream_set_blocking(socket, False)
            
            
            timeoutS  = intval(timeout)
            timeoutUs = (timeout - timeoutS)  100000
            stream_set_timeout(socket, timeoutS, timeoutUs)
            
            fwrite(socket, request)
            
            if( not self.config.getFireAndForget()) 
                while( not feof(socket)) 
                    response .= fgets(socket, 512)
                
            
            
            fclose(socket)


        if(loggingCallback = self.config.getLoggingCallback()) 
            loggingCallback(request, response)


        return response


    """ 
    Simply delegates to send() if config option "sendOnShutdown" is disabled
    or enqueues the request by registering a PHP shutdown function.
    """
    def fire(self):
        if(self.config.getSendOnShutdown()) 
            # This dumb variable assignment is needed as PHP prohibits using
            # this in closure use statements
            instance = this
            # We use a closure here to retain the current values/states of
            # this instance and request (as the use statement will copy them
            # into its own scope)
            register_shutdown_function(function() use(instance) 
                instance._send()
            )
         else:
            self._send()





