

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
This is nearly a 1:1 PHP port of the gaforflash X10 class code.:

@link http://code.google.com/p/gaforflash/source/browse/trunk/src/com/google/analytics/data/X10.as
"""
class X10(object):
    """ 
    @var string
    """
    KEY = 'k'

    """ 
    @var string
    """
    VALUE = 'v'

    """ 
    @var array
    """
    SET = [KEY, VALUE]

    """ 
    Opening delimiter for wrapping a set of values belonging to the same type.
    @var string
    """
    DELIM_BEGIN = '('

    """ 
    Closing delimiter for wrapping a set of values belonging to the same type.
    @var string
    """
    DELIM_END   = ')'

    """ 
    Delimiter between two consecutive num/value pairs.
    @var string
    """
    DELIM_SET = ''

    """ 
    Delimiter between a num and its corresponding value.
    @var string
    """
    DELIM_NUM_VALUE = '!'

    """ 
    Mapping of escapable characters to their escaped forms.

    @var array
    """
    ESCAPE_CHAR_MAP = {
    "'": "'0",
    ')': "'1",
    '*': "'2",
    '!': "'3",
    }

    """ 
    @var int
    """
    MINIMUM = 1

    OBJECT_KEY_NUM  = 1
    TYPE_KEY_NUM    = 2
    LABEL_KEY_NUM   = 3
    VALUE_VALUE_NUM = 1


    def __init__(self):
        projectData = {}


    """ 
    @param int projectId
    @return bool
    """
    def hasProject(self, projectId):
        return isset(self.projectData[projectId])


    """ 
    @param int projectId
    @param int num
    @param mixed value
    """
    def hasProject(self, projectId, num, value):
        self.setInternal(projectId, self.KEY, num, value)


    """ 
    @param int projectId
    @param int num
    @return mixed
    """
    def getKey(self, projectId, num):
        return self.getInternal(projectId, self.KEY, num)


    """ 
    @param int projectId
    """
    def clearKey(self, projectId):
        self.clearInternal(projectId, self.KEY)


    """ 
    @param int projectId
    @param int num
    @param mixed value
    """
    def setValue(self, projectId, num, value):
        self.setInternal(projectId, self.VALUE, num, value)


    """ 
    @param int projectId
    @param int num
    @return mixed
    """
    def getValue(self, projectId, num):
        return self.getInternal(projectId, self.VALUE, num)


    """ 
    @param int projectId
    """
    def clearValue(self, projectId):
        self.clearInternal(projectId, self.VALUE)


    """ 
    Shared internal implementation for setting an X10 data type.

    @param int projectId
    @param string type
    @param int num
    @param mixed value
    """
    def setInternal(self, projectId, type, num, value):
        if projectId not in self.projectData:
            self.projectData[projectId] = {}

        if type not in self.projectData[projectId]:
            self.projectData[projectId][type] = {}

        self.projectData[projectId][type][num] = value


    """ 
    Shared internal implementation for getting an X10 data type.

    @param int projectId
    @param string type
    @param int num
    @return mixed
    """
    def getInternal(self, projectId, type, num):
        return self.projectData[projectId][type].get(num, None)


    """ 
    Shared internal implementation for clearing all X10 data of a type from a
    certain project.

    @param int projectId
    @param string type
    """
    def clearInternal(self, projectId, type):
        try:
            del self.projectData[projectId][type]
        except KeyError:
            pass


    """ 
    Escape X10 string values to remove ambiguity for special characters.

    @see X10::escapeCharMap
    @param string value
    @return string
    """
    def escapeExtensibleValue(self, value):
        result = ''
        length = len(value)
        for i in range(length):
            char = value[i]
            result += X10.ESCAPE_CHAR_MAP.get(char, char)

        return result


    """ 
    Given a data array for a certain type, render its string encoding.

    @param array data
    @return string
    """
    def renderDataType(self, data):
        result = []

        lastI = 0
        ksort(data, SORT_NUMERIC)
        sorted_data = sorted(data.items(), key=lambda x: x[1])
        for i, entry in sorted_data:
            if entry:
                str = ''
                
                # Check if we need to append the number. If the last number was
                # outputted, or if this is the assumed minimum, then we don't.
                if i != self.MINIMUM and i - 1 != lastI:
                    str += i
                    str += self.DELIM_NUM_VALUE
                
                str += self.escapeExtensibleValue(entry)
                result.append(str)
            
            lastI = i

        return X10.DELIM_BEGIN + X10.DELIM_SET.join(result) + self.DELIM_END


    """ 
    Given a project array, render its string encoding.

    @param array project
    @return string
    """
    def renderProject(self, project):
        result = ''

        # Do we need to output the type string? As an optimization we do not
        # output the type string if it's the first type, or if the previous
        # type was present.
        needTypeQualifier = False

        length = len(X10.SET)
        for i in range(length):
            if project[self.SET].get(i):
                data = project[self.SET[i]]
                
                if needTypeQualifier:
                    result += self.SET[i]
                
                result += self.renderDataType(data)
                needTypeQualifier = False
            else:
                needTypeQualifier = True
            
        return result


    """ 
    Generates the URL parameter string for the current internal extensible data state.

    @return string
    """
    def renderUrlString(self):
        result = ''

        for projectId, project in self.projectData.iteritems():
            result += projectId + self.renderProject(project)

        return result




