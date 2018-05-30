''' AtCore
    Copyright (C) <2018>

    Authors:
        Patrick Jose Pereira <patrickelectric@gmail.com>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) version 3, or any
    later version accepted by the membership of KDE e.V. (or its
    successor approved by the membership of KDE e.V.), which shall
    act as a proxy defined in Section 6 of version 3 of the license.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
import urllib.request

data = urllib.request.urlopen('https://raw.githubusercontent.com/repetier/Repetier-Firmware/master/src/ArduinoDUE/Repetier/Repetier.ino')
if not data:
    print('No data available')
    exit(1)


# Check for GX-XXX or MX-XXX
gcode_regex = None
gcode_regex = re.compile('- [G,M]\d{1,3}')

gcode_dict = []
string_offset = len('- ')
gcode_code = ''
gcode_args = ''
gcode_description = ''

for line in data:

    # Convert bytes to string
    line = line.decode("utf-8")

    result = gcode_regex.match(line)
    if not result:
        continue

    gcode_code = line[result.start() + 2: result.end()]
    after_gcode = line[result.end() + 1:-1]
    if len(after_gcode.split('-')) > 1:
        gcode_args = after_gcode.split('-')[0]
        gcode_description = after_gcode.split('-')[1]
    print('| %s | %s | %s |' % (gcode_code, gcode_args, gcode_description))



