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

import json
import re
import urllib.request
import yaml

print('start')
json_str = urllib.request.urlopen('https://api.github.com/repos/MarlinFirmware/MarlinDocumentation/contents/_gcode')
data = json.loads(json_str.read())

gcode_code = ''
gcode_args = ''
gcode_description = ''

for item in data:
    #print(item['download_url'])
    response = urllib.request.urlopen(item['download_url']).read().decode('utf-8')
    yaml_string = response.split('---\n')[1]
    #try:
    gcode_yaml = yaml.load(yaml_string)
    #print(yaml.dump(gcode_yaml))

    #print(gcode_yaml['codes'], gcode_yaml['brief'])
    gcode_code = ', '.join(gcode_yaml['codes'])
    gcode_description = gcode_yaml['brief']
    gcode_args = ''
    if 'parameters' in gcode_yaml:
        if not gcode_yaml['parameters']:
            print('| %s | %s | %s |' % (gcode_code, gcode_args, gcode_description))
            continue
        for parameter in gcode_yaml['parameters']:
            parameter_type = None
            if 'values' in parameter:
                if type(parameter['values']) == list:
                    if 'type' in parameter['values'][0]:
                        parameter_type = parameter['values'][0]['type']
                    else:
                        #print('>', parameter['values'][0])
                        parameter_type = parameter['values'][0]['tag']
                else:
                    if parameter['values']:
                        if 'type' in parameter['values']:
                            parameter_type = parameter['values']['type']
                        else:
                            if 'tag' in parameter['values']:
                                #print('>', parameter['values'])
                                parameter_type = parameter['values']['tag']
                            else:
                                pass
                                #print('wtf', parameter['values'])
            else:
                if type(parameter) == list:
                    if 'type' in parameter[0]:
                        parameter_type = parameter[0]['type']
                    else:
                        #print('>', parameter[0])
                        parameter_type = parameter[0]['tag']
                else:
                    if 'type' in parameter:
                        parameter_type = parameter['type']
                    else:
                        if 'tag' in parameter:
                            #print('>', parameter)
                            parameter_type = parameter['tag']
                        else:
                            pass
                            #print('wtf', parameter)

            if 'tag' in parameter:
                gcode_args += '%s`<%s>` ' % (parameter['tag'], parameter_type)
            else:
                gcode_args += '%s ' % (parameter_type)
    print('| %s | %s | %s |' % (gcode_code, gcode_args, gcode_description))
    '''
    except Exception as e:
        print(e)
        print(yaml_string)
        exit(1)
    '''

exit(1)

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