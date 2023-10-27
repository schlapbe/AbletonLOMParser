from elements import dic

group_tags = ["Method", "Value", "Property", "listener Method"]
group_names = ["Methods", "Values", "Properties", "Listeners"]


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []


def build_tree_recursive_with_groups_as_children(elements, parent_id=None, level=0, max_depth=6):
    if level > max_depth:
        return []
    tree_nodes = []
    group_nodes = {}
    for element in elements:
        if element["ref_parent"] == parent_id:
            node = TreeNode(element)
            children = build_tree_recursive_with_groups_as_children(elements, parent_id=element["ref"], level=level + 1,
                                                                    max_depth=max_depth)
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
        description = f'full path:{fullpath}\n\n{description}'
        outline = f'{indent}<outline text="{name}" _note="{description}" type="label" _label="{tag}">\n'
    for child_node in node.children:
        outline += generate_outline(child_node, depth + 1)
    outline += f'{indent}</outline>\n'
    return outline


def export_to_opml(tree_nodes, file_path):
    opml_header = '''<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n<head>\n<title>Tree Export</title>\n
    </head>\n<body>'''
    opml_footer = '''</body>\n</opml>'''
    outlines = ""
    for node in tree_nodes:
        outlines += generate_outline(node)
    opml_content = opml_header + outlines + opml_footer
    with open(file_path, "w") as f:
        f.write(opml_content)
    return opml_content


def main():
    # tree_nodes = build_tree_recursive(dic)
    tree_nodes = build_tree_recursive_with_groups_as_children(dic)
    export_to_opml(tree_nodes, "tree_export.opml")
    # selected_tags = ["Method", "Value", "Property", "listener Method"]


if __name__ == "__main__":
    main()
