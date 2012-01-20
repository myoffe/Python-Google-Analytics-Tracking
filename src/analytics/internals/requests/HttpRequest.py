

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
import urllib
import urllib2

from analytics import Config
from analytics.internals import utils



# @link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/GIFRequest.as
class HttpRequest(object):

    def __init__(self, config=None):
        # Indicates the type of request, will be mapped to "utmt" parameter
        # @see ParameterHolder::utmt
        # @var string
        self.type = None

        self.config = None
        self.x_forwarded_for = None
        self.userAgent = None

        self.setConfig(config or Config())
    

    def getConfig(self):
        return self.config


    def setConfig(self, config):
        self.config = config


    def setx_forwarded_for(self, value):
        self.x_forwarded_for = value


    def setUserAgent(self, value):
        self.userAgent = value

    def buildHttpRequest(self):
        parameters = self.build_parameters()
        query_string = urllib.urlencode(parameters)
        url = self.config.get_endpoint_host() + self.config.get_endpoint_path()

        # Mimic Javascript's encodeURIComponent() encoding for the query
        # string just to be sure we are 100% consistent with GA's Javascript client
        query_string = utils.convert_to_uri_component_encoding(query_string)

        # Recent versions of ga.js use HTTP POST requests if the query string is too long
        usePost = len(query_string) > 2036

        if not usePost:
            req = urllib2.Request(url + '?' + query_string)
        else:
            req = urllib2.Request(url, data=query_string)

        if self.userAgent:
            req.add_header('User-Agent', self.userAgent.replace('\n','').replace('\r',''))

        if self.x_forwarded_for:
            # Sadly "X-Forwarded-For" is not supported by GA so far,
            # see e.g. http://www.google.com/support/forum/p/Google+Analytics/thread?tid=017691c9e71d4b24,
            # but we include it nonetheless for the pure sake of correctness (and hope)
            # TODO do I need the \r\n replaces?
            req.add_header('X-Forwarded-For', self.x_forwarded_for.replace('\n','').replace('\r',''))

        if usePost:
            # Don't ask me why "text/plain", but ga.js says so :)
            req.add_header('Content-Type', 'text/plain')
            req.add_header('Content-Length', str(len(query_string)))

        return req


    def build_parameters(self):
        raise NotImplementedError()


    def _send(self):
        """
        This method should only be called directly or indirectly by fire(), but must
        remain public as it can be called by a closure function.

        Sends either a normal HTTP request with response or an asynchronous request
        to Google Analytics without waiting for the response. Will always return
        null in the latter case, or false if any connection problems arise.

        @return null|string|bool
        """
        request = self.build_http_request()
        response = None

        # Do not actually send the request if endpoint host is set to None
        if self.config.get_endpoint_host():
            timeout = self.config.request_timeout

            if self.config.getFireAndForget():
                raise NotImplementedError('Asynchronous send not implemented yet')

            # TODO Handle errors?
            response = urllib2.urlopen(request, timeout=timeout).read()

        logging_callback = self.config.logging_callback
        if logging_callback:
            logging_callback(request, response)


        return response


    def fire(self):
        if self.config.send_on_shutdown:
            import atexit
            atexit.register(lambda: self._send())
        else:
            self._send()





