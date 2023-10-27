from elements import dic


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

def build_tree_recursive(elements, parent_id=None, level=0, max_depth=6):
    if level > max_depth:
        return None
    tree_nodes = []
    for element in elements:
        if element["ref_parent"] == parent_id:
            node = TreeNode(element)
            children = build_tree_recursive(elements, parent_id=element["ref"], level=level + 1, max_depth=max_depth)
            if children:
                node.children.extend(children)
            tree_nodes.append(node) 
    return tree_nodes

def export_to_opml(tree_nodes, file_path):
    opml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
<head>
    <title>Tree Export</title>
</head>
<body>
'''

    opml_footer = '''</body>
</opml>
'''

    def generate_outline(node, depth=0):
        indent = '    ' * depth
        description = node.data["description"]
        if description != None:
            description.replace('"','&quot;')
            description.replace("'",'&quot;')
        outline = f'{indent}<outline text="{node.data["name"]}" _note="{description}" id="{node.data["ref"]}" type="label" _label="{node.data["tag"]}">\n'
        for child_node in node.children:
            outline += generate_outline(child_node, depth + 1)
        outline += f'{indent}</outline>\n'
        return outline


    outlines = ""
    for node in tree_nodes:
        outlines += generate_outline(node)

    opml_content = opml_header + outlines + opml_footer

    with open(file_path, "w") as f:
        f.write(opml_content)



if __name__ == "__main__":
    tree_nodes = build_tree_recursive(dic)
    export_to_opml(tree_nodes, "tree_export.opml")
pass
