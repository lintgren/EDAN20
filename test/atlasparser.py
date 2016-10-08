import sys

import xml.etree.ElementTree as ET

tree = ET.parse("greySheet.xml")

root = tree.getroot()

f = open("greySheet.atlas", 'w')

f.write('\n' + root.get('imagePath'))

f.write('\nformat: RGBA8888\nfilter: Nearest,Nearest\nrepeat: none\n')

for texture in root:

    f.write(texture.get('name') + '\n  rotate: false\n')

    f.write('  xy: ' + texture.get('x') + ', ' + texture.get('y') + '\n')

    f.write('  size: ' + texture.get('width') + ', ' + texture.get('height') + '\n')

    f.write('  orig: ' + texture.get('width') + ', ' + texture.get('height') + '\n')

    f.write('  offset: 0, 0\n  index: -1\n')

f.close