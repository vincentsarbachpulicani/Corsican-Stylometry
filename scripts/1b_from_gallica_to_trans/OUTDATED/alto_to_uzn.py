import codecs
import os
import sys
import xml.etree.ElementTree as ET

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
             'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
             'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}
tree = ET.parse(sys.argv[1])
xmlns = tree.getroot().tag.split('}')[0].strip('{')
if xmlns in namespace.values():
    with open("test.uzn", "a+") as f:
        for lines in tree.iterfind('.//{%s}TextBlock' % xmlns):
            #sys.stdout.write('\n')
            text = line.attrib.get('HPOS') + ' ' + line.attrib.get('VPOS') + ' ' + line.attrib.get('WIDTH') + ' ' + line.attrib.get('HEIGHT') + line.attrib.get('ID') + ' ' + '\n'
            f.write(text)
else:
    print('ERROR: Not a valid ALTO file (namespace declaration missing)')
