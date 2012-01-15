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
Note: Doesn't necessarily have to be consistent across requests, as it doesn't
alter the actual tracking result.

@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/core/GIFRequest.as
"""

class ConfigurationError(Exception):
    pass


class Config(object):
  ERROR_SEVERITY_SILENCE    = 0
  ERROR_SEVERITY_WARNINGS   = 1
  ERROR_SEVERITY_EXCEPTIONS = 2
  """ 
  Ignore all errors completely.
  """
  
  """ 
  Trigger PHP errors with a E_USER_WARNING error level.
  """
  
  """ 
  Throw UnitedPrototype\GoogleAnalytics\Exception exceptions.
  """

  """ 
    How strict should errors get handled? After all, we do just do some
    tracking stuff here, and errors shouldn't break an application's
    functionality in production.
    RECOMMENDATION: Exceptions during deveopment, warnings in production.

    Assign any value of the ERROR_SEVERITY_ constants.

    @see Tracker::_raiseError()
    @var int
  """

  """ 
  Whether to just queue all requests on HttpRequest::fire() and actually send
  them on PHP script shutdown after all other tasks are done.

  This has two advantages:
  1) It effectively doesn't affect app performance
  2) It can e.g. handle custom variables that were set after scheduling a request

  @see Internals\Request\HttpRequest::fire()
  @var bool
  """
    
  """ 
  Whether to make asynchronous requests to GA without waiting for any
  response (speeds up doing requests).

  @see Internals\Request\HttpRequest::send()
  @var bool
  """

  """ 
  Logging callback, registered via setLoggingCallback(). Will be fired
  whenever a request gets sent out and receives the full HTTP request
  as the first and the full HTTP response (or null if the "fireAndForget"
  option or simulation mode are used) as the second argument.

  @var \Closure
  """

  """ 
  Seconds (float allowed) to wait until timeout when connecting to the
  Google analytics endpoint host

  @see Internals\Request\HttpRequest::send()
  @var float
  """

  # FIXME: Add SSL support, https:#ssl.google-analytics.com

  """ 
  Google Analytics tracking request endpoint host. Can be set to null to
  silently simulate (and log) requests without actually sending them.

  @see Internals\Request\HttpRequest::send()
  @var string
  """

  """ 
  Google Analytics tracking request endpoint path

  @see Internals\Request\HttpRequest::send()
  @var string
  """

  """ 
  Whether to anonymize IP addresses within Google Analytics by stripping
  the last IP address block, will be mapped to "aip" parameter

  @see Internals\ParameterHolder::aip
  @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApi_gat.html#_gat._anonymizeIp
  @var bool
  """

  """ 
  Defines a sample set size (0-100) for Site Speed data collection.
  By default, a fixed 1% sampling of your site visitors make up the data pool from which
  the Site Speed metrics are derived.

  @see Page::loadTime
  @link http://code.google.com/apis/analytics/docs/gaJS/gaJSApiBasicConfiguration.html#_gat.GA_Tracker_._setSiteSpeedSampleRate
  @var int
  """
    

  """ 
  @param array properties
  """
  def __init__(self, properties):
    self.errorSeverity = Config.ERROR_SEVERITY_EXCEPTIONS
    self.sendOnShutdown = False
    self.fireAndForget = False
    self.loggingCallback = None
    self.requestTimeout = 1
    self.endPointHost = 'www.google-analytics.com'
    self.endPointPath = '/__utm.gif'
    self.anonymizeIpAddresses = False
    self.sitespeedSampleRate = 1

    for prop, value in properties.items():
      setterName = 'set' + prop
      setter = getattr(self, setterName)
      if setter:
        setter(value)
      else:
        raise ConfigurationError('There is no setting %s' % prop)
         

  """ 
  @return int See self::ERROR_SEVERITY_ constants
  """
  def getErrorSeverity(self):
    return self.errorSeverity


  """ 
  @param int errorSeverity See self::ERROR_SEVERITY_ constants
  """
  def setErrorSeverity(self, errorSeverity):
    self.errorSeverity = errorSeverity


  """ 
  @return bool
  """
  def getSendOnShutdown(self):
    return self.sendOnShutdown


  """ 
  @param bool sendOnShutdown
  """
  def setSendOnShutdown(self, sendOnShutdown):
    self.sendOnShutdown = sendOnShutdown


  """ 
  @return bool
  """
  def getFireAndForget(self):
    return self.fireAndForget


  """ 
  @param bool fireAndForget
  """
  def setFireAndForget(self, fireAndForget):
    self.fireAndForget = fireAndForget


  """ 
  @return \Closure|null
  """
  def getLoggingCallback(self):
    return self.loggingCallback


  """ 
  @param \Closure callback
  """
  def setLoggingCallback(self, callback):
    self.loggingCallback = callback


  """ 
  @return float
  """
  def getRequestTimeout(self):
    return self.requestTimeout


  """ 
  @param float requestTimeout
  """
  def setRequestTimeout(self, requestTimeout):
    self.requestTimeout = requestTimeout


  """ 
  @return string|null
  """
  def getEndPointHost(self):
    return self.endPointHost


  """ 
  @param string|null endPointHost
  """
  def setEndPointHost(self, endPointHost):
    self.endPointHost = endPointHost


  """ 
  @return string
  """
  def getEndPointPath(self):
    return self.endPointPath


  """ 
  @param string endPointPath
  """
  def setEndPointPath(self, endPointPath):
    self.endPointPath = endPointPath


  """ 
  @return bool
  """
  def getAnonymizeIpAddresses(self):
    return self.anonymizeIpAddresses


  """ 
  @param bool anonymizeIpAddresses
  """
  def setAnonymizeIpAddresses(self, anonymizeIpAddresses):
    self.anonymizeIpAddresses = anonymizeIpAddresses


  """ 
  @return int
  """
  def getSitespeedSampleRate(self):
    return self.sitespeedSampleRate


  """ 
  @param int sitespeedSampleRate
  """
  def setSitespeedSampleRate(self, sitespeedSampleRate):
    if sitespeedSampleRate != sitespeedSampleRate or sitespeedSampleRate < 0 or sitespeedSampleRate > 100:
        return ValueError('For consistency with ga.js, sample rates must be specified as a number between 0 and 100.')
    
    self.sitespeedSampleRate = sitespeedSampleRate
