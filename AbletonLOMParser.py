# xml Parser for Ableton's Live Object Model
# to export it to OPML and possible other formats

import xml.etree.ElementTree as Element_Tree
import os, sys

# from opml import OpmlDocument

group_tags = ["Method", "Value", "Property", "listener Method"]
group_names = ["Methods", "Values", "Properties", "Listeners"]
listener_groups = ["add", "remove", "has"]


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []


class AbletonLOM:
    def __init__(self):
        self.is_imported_from_xml = False
        self.sorted = False
        self.elements = []
        self.tags = []
        self.root = None
        self.skip_tag = "Doc"
        self.group_tags = ["Method", "Value", "Property", "listener Method"]
        self.listenermethods = ['add_', 'remove_', "_has_listener"]
        self.parsed_children = None

    @staticmethod
    def parse_path(text):
        return text.split(".")

    def import_from_xml_tree(self, xml_tree):
        self.root = xml_tree.getroot()
        self.get_tags()
        ref = 0
        for i in range(0, len(self.root)):
            name = self.root[i].text
            description = self.get_doc(self.root, i)
            if description is not None:
                description = description.replace("\t", '')
                description = description.replace('"', '&quot;')
            description = 'None for now'
            path = self.parse_path(name)
            tag = self.root[i].tag
            if path[-1].endswith("listener()"):
                listener_method = True
                tag = "listener Method"
            else:
                listener_method = False
            if tag in self.group_tags:
                group = tag
            else:
                group = None
            e_dic = {"ref": ref, "tag": tag, "name": name, "description": description, "path": path,
                     "hierarchy": len(path) - 1, "ref_parent": None, "children": [], "group": group}
            if tag != self.skip_tag:
                self.elements.append(e_dic)
                ref += 1
        self.is_imported_from_xml = True

    @staticmethod
    def get_doc(root, pos):
        try:
            if len(root)-1 > pos:
                if root[pos + 1].tag == "Doc":
                    return root[pos + 1].text
                else:
                    return None
        except Exception as e:
            print(f"{e} has occurred, pos:{pos}, length of root: {len(root)}")
            return None

    def get_tags(self):
        self.tags = []
        for element in self.root:
            if element.tag not in self.tags:
                self.tags.append(element.tag)

    def clean_up_description(self):
        # this func will clean description from tabs,
        # and split up the syntax and C++ signature etc
        pass

    def get_parent_references(self):
        for element in self.elements:
            if len(element['path']) > 1:
                try:
                    parent_path = element['path'][0:-1]
                    res = list(filter(lambda search: search['path'] == parent_path, self.elements))[0]
                    if res is not None:
                        element["ref_parent"] = res['ref']
                except Exception as e:
                    print(f'Error: {e}, element: {element}')

    def get_children_references(self):
        for element in self.elements:
            ref = element['ref']
            for child in self.elements:
                if child['ref_parent'] == ref:
                    element['children'].append(child['ref'])

    def get_classes(self):
        return list(filter(lambda s_class: s_class['tag'] == 'Class', self.elements))

    def get_class_with_methods(self, class_dic):
        ref = class_dic['ref']
        return list(filter(lambda elements: elements['ref_parent'] == ref, self.elements))

    def get_children(self, parent_dic):
        children_ref = parent_dic['children']
        children_list = []
        for i in range(0, len(children_ref)):
            children_list.append(self.elements[children_ref[i]])
        return children_list

    def rec_get_all_children(self, parent_id, pr_children, level=0):
        children = self.elements[parent_id]['children']
        if children is []:
            return children
        else:
            for child in children:
                if child['ref'] not in self.parsed_children:
                    self.parsed_children.append(child['ref'])
            pass

    def print_dic(self):
        new_dic = []
        for element in self.elements:
            dic = {'ref': element['ref'], 'children': element['children']}
            new_dic.append(dic)
        return new_dic

    def print_children_to_file(self, filename, print_txt=True):
        # new_dic = self.print_dic()
        with open(filename + ".py", 'w') as f:
            f.write(f'dic={str(self.elements)}')
        if print_txt:
            with open(filename + "_testdiic.py", 'w') as f:
                f.write(f"dic = [ \n")
                for line in self.elements:
                    # f.write(f"{line['name']}, \nTag: {line['tag']}, Group: {line['group']}, Ref: {line['ref']}\n")
                    # if "listener" in str(line['group']):
                    f.write(f"{line},\n")
                f.write(f"] \n")
        return self.elements

def build_tree_recursive_with_groups_as_children(elements, parent_id=None, level=0, max_depth=6):
    if level > max_depth:
        return []
    tree_nodes = []
    group_nodes = {}
    for element in elements:
        if element["ref_parent"] == parent_id:
            node = TreeNode(element)
            children = build_tree_recursive_with_groups_as_children(elements, parent_id=element["ref"], level=level + 1, max_depth=max_depth)
            if children:
                node.children.extend(children)
            group = element.get("group")
            if group:
                if group not in group_nodes:
                    dic = {"name": f"Group: {group}", "id": f"group_{group}", "tag": group, "group": group}
                    group_nodes[group] = TreeNode(dic)
                group_nodes[group].children.append(node)
            else:
                tree_nodes.append(node)
    for group_node in group_nodes.values():
        tree_nodes.append(group_node)
    return tree_nodes


def output_tree(filename, tree):
    filename = filename + '-tree.txt'
    with open(filename, "w") as file:
        root = tree.getroot()
        for element in root:
            file.write(f"{Element_Tree.tostring(element)} \n")


def generate_outline(node, depth=0):
    indent = '    ' * depth
    fullpath = node.data["name"]
    tag = node.data['tag']
    if "Group" in fullpath:
        # description = None
        name = node.data['tag']
        for i in range(0, len(group_tags)):
            if name == group_tags[i]:
                name = group_names[i]
                break
        outline = f'{indent}<outline text="{name}">\n'
    else:
        name = node.data["path"][-1]
        description = node.data["description"]
        if description is not None:
            description.replace('"', '&quot;')
            description.replace("'", '&quot;')
        else:
            description = ""
        description = f'full path:{fullpath}\\n{description}'
        outline = f'{indent}<outline text="{name}" _note="{description}" type="label" _label="{tag}">\n'
    for child_node in node.children:
        outline += generate_outline(child_node, depth + 1)
    outline += f'{indent}</outline>\n'
    return outline


def export_to_opml(tree_nodes, file_path):
    opml_header = '''<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n<head>\n\t<title>Tree Export</title>\n</head>\n<body>'''
    opml_footer = '''</body>\n</opml>'''
    outlines = ""
    for node in tree_nodes:
        outlines += generate_outline(node)
    opml_content = opml_header + outlines + opml_footer
    with open(file_path, "w") as f:
        f.write(opml_content)
    return opml_content


def get_xml_file():
    if len(sys.argv) < 2:
        return "./examples/Live12"
    filename = sys.argv[1]
    if not filename.endswith(".xml"):
        sys.exit("Not a XML file")
    if not os.path.isfile(filename):
        sys.exit("File does not exist")
    filename = filename.split(".xml")
    # print(filename[0]))
    return filename[0]


def main():
    filename = get_xml_file()
    filename_xml = str(filename) + ".xml"
    with open(filename_xml) as file:
        tree = Element_Tree.parse(file)
        output_tree(filename, tree)
    lom = AbletonLOM()
    lom.import_from_xml_tree(tree)
    # lom.get_parent_references()
    # lom.get_children_references()
    dic = lom.print_children_to_file(filename, True)
    tree_nodes = build_tree_recursive_with_groups_as_children(dic)
    export_to_opml(tree_nodes, filename + ".opml")


if __name__ == "__main__":
    main()
