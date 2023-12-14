# xml Parser for Ableton's Live Object Model
# to export it to OPML and possible other formats

import xml.etree.ElementTree as Element_Tree
import os
import sys

# from opml import OpmlDocument

group_tags = ["Method", "Value", "Property", "Listener Method", "Listener"]
group_names = ["Methods", "Values", "Properties", "Listener Methods", "Listener"]


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
        self.parsed_children = None

    @staticmethod
    def parse_path(text):
        return text.split(".")

    # this method parses the imported xml file
    # into a customised dictionary
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
            path = self.parse_path(name)
            tag = self.root[i].tag
            if path[-1].endswith("listener()"):
                tag = "Listener Method"
            if tag in group_tags:
                group = tag
            else:
                group = None
            e_dic = {"ref": ref,
                     "tag": tag,
                     "name": name,
                     "description": description,
                     "path": path,
                     "hierarchy": len(path) - 1,
                     "ref_parent": None,
                     "children": [],
                     "group": group,
                     "listener_ref": None}
            # this is needed since Live 11.3
            # there are some weired unnamed python methods, which are not documented
            # if this is the case, the entry is skipped
            if "Boost.Python" in name:
                continue
            if tag != self.skip_tag:
                self.elements.append(e_dic)
                ref += 1
        self.elements = self.summarize_listener_methods(self.elements)
        self.is_imported_from_xml = True

    # returns listener name
    @staticmethod
    def get_listener_name(listener_name):
        patterns = ['add_', '_listener()', '_has', 'remove_']
        if listener_name.startswith("add_") or listener_name.startswith("remove_"):
            stripped_name = listener_name.split("_")
            pure_listener_name = "_".join(stripped_name[1:-1])
            return pure_listener_name
        if listener_name.endswith("has_listener()"):
            stripped_name = listener_name.split("_")
            pure_listener_name = "_".join(stripped_name[0:-2])
            return pure_listener_name

    # compares two different api paths and returns True, if it refers to the same listener
    def compare_listener_path(self, ref_path, target_path):
        if self.get_listener_name(ref_path) == self.get_listener_name(target_path):
            return True
        return False

    def summarize_listener_methods(self, dic):
        listener_methods = None
        new_refs = len(dic) - 1
        for element in dic:
            # check if listener, if not skip
            if element["group"] != "Listener Method":
                continue
            # check if listener group is already there:
            if "listener" in element["path"][-1]:
                # print("listener Method found")
                new_refs += 1
                existing_listener = False
                listener_name = element["path"][-1]
                new_path = element["path"]
                # new_path[-1] = self.get_listener_name(listener_name) + " - Listener"
                summarized_entry = {
                    "ref": new_refs,  # Assign a new reference number
                    "tag": "Listener",
                    "name": self.get_listener_name(listener_name),
                    "description": element["description"],
                    "path": new_path,
                    "hierarchy": element["hierarchy"],
                    "ref_parent": element["ref_parent"],
                    "children": None,  # References to individual listener methods
                    "group": "Listener",
                    "listener_ref": element["ref"]
                }
                if listener_methods:
                    for listener_search in listener_methods:
                        # print(listener_name)
                        if self.compare_listener_path(listener_search['path'][-1], element["path"][-1]):
                            if isinstance(listener_search['listener_ref'], int):
                                listener_search['listener_ref'] = [listener_search['listener_ref'], element['ref']]
                                existing_listener = True
                            elif isinstance(listener_search['listener_ref'], list):
                                listener_search['listener_ref'].append(element['ref'])
                                existing_listener = True
                                break
                    if not existing_listener:
                        listener_methods.append(summarized_entry)
                else:
                    listener_methods = [summarized_entry]
        # print(listener_methods)
        for new_listener in listener_methods:
            dic.append(new_listener)
        return dic

    @staticmethod
    def get_doc(root, pos):
        try:
            if len(root) - 1 > pos:
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

    # this method refers all parents in the paths to be able to build a tree structure later
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

    # this method refers all children in the paths to be able to build a tree structure later
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
        with open(filename + "_dic.py", 'w') as f:
            f.write(f"dic = [ \n")
            for line in self.elements:
                f.write(f"{line},\n")
            f.write(f"] \n")


def build_tree_recursive_with_groups_as_children(elements, parent_id=None, level=0):
    tree_nodes = []
    group_nodes = {}
    for element in elements:
        if element["ref_parent"] == parent_id:
            node = TreeNode(element)
            children = build_tree_recursive_with_groups_as_children(elements, parent_id=element["ref"], level=level + 1)
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


def clean_description_for_X_Mind(description, full_path):
    # convert \ns
    if description:
        description = description.replace('"', '&quot;')
        description = description.replace("'", '&quot;')
        # description = description.replace("-&gt;", '-&gt: &#10;')
        description = description.replace('\n', ' &#10;&#10;')
        description = description.replace('C++ signature :', ' &#10;&#10;C++ signature:')
        description = description.replace('void', 'void &#10;')
    return f"full path:&#10;{full_path} &#10; &#10; {description}"


def generate_outline(node, depth=0):
    indent = '    ' * depth
    # fullpath = node.data["name"]
    tag = node.data['tag']
    if "Group" in node.data['name']:
        # description = None
        name = node.data['tag']
        for i in range(0, len(group_tags)):
            if name == group_tags[i]:
                name = group_names[i]
                break
        outline = f'{indent}<outline text="{name}">\n'
    else:
        # name = node.data['name']
        fullpath = "".join(node.data['path'])
        description = clean_description_for_X_Mind(node.data["description"], fullpath)
        lastname = node.data["path"][-1]
        if node.data['group'] == 'Listener':
            lastname = node.data['name']
        outline = f'{indent}<outline text="{lastname}" _note="{description}" type="label" _label="{tag}">\n'
    for child_node in node.children:
        outline += generate_outline(child_node, depth + 1)
    outline += f'{indent}</outline>\n'
    return outline


def export_to_opml(tree_nodes, file_path):
    opml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n<head>\n\t<title>Tree Export</title>\n</head>\n<body>'
    opml_footer = '</body>\n</opml>'
    outlines = ""
    for node in tree_nodes:
        outlines += generate_outline(node)
    opml_content = opml_header + outlines + opml_footer
    with open(file_path, "w") as f:
        f.write(opml_content)
    return opml_content


def get_xml_file():
    if len(sys.argv) < 2:
        return "./examples/Live_shrinked"
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
        if "--treetxt" in sys.argv:
            output_tree(filename, tree)
    lom = AbletonLOM()
    lom.import_from_xml_tree(tree)
    lom.get_parent_references()
    lom.get_children_references()
    tree_nodes = build_tree_recursive_with_groups_as_children(lom.elements)
    if "--dictofile" in sys.argv:
        lom.print_children_to_file(filename, True)
    export_to_opml(tree_nodes, filename + ".opml")


if __name__ == "__main__":
    main()
