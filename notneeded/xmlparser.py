import xml.etree.ElementTree as ET
import os
# from opml import Opml

document = OpmlDocument()
basicpath = os.getcwd()+"/finalproject/livexml/"
print(basicpath)
tags = ["Built-In","Method","Class","Property"]

with open(basicpath+'Live11.xml') as file:
    tree = ET.parse(file)
    root = tree.getroot()
    print(len(root))
    properties = []
    methods = []
    classes = []
for i in range(0,len(root)):
    # print(f'{element.tag}: {element.text}')
    element = root[i]
    if element.tag == 'Property':
        if root[i+1].tag == "Doc":
            description = root[i+1].text
        else:
            description = None
        dic = {"name" : element.text, "description" : description}
        properties.append(dic)

    if element.tag == 'Method':
        if root[i+1].tag == "Doc":
            description = root[i+1].text
        else:
            description = None
        dic = {"name": element.text, "description" : description}
        methods.append(dic)

    if element.tag == 'Class':
        if root[i+1].tag == "Doc":
            description = root[i+1].text
        else:
            description = None
        dic = {"name" : element.text, "description" : description}
        classes.append(dic)

# print(f"Property: {properties[23]['property']}\nDescription: {properties[23]['description']}")
# print()
# print(f"Method: {methods[23]['method']}\nDescription: {methods[23]['description']}")

for element in classes:
    print(f"Class: {element['name']}")

print(f"Methods: {len(methods)}")
print(f"Classes: {len(classes)}")
print(f"Properties: {len(properties)}")
