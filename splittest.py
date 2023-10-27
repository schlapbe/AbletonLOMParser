text = "Live.Application.Application.View.toggle_browse()"
path = list(text.split("."))
# print(path)
# Live.Application.Application.View.remove_view_focus_changed_listener()

start_dic = [
    {"tag": "Class", "name" : "Application", "path": ['Live', 'Application', 'Application'], "ref" : 1},
    {"tag": "Class", "name" : "Song", "path": ['Live', 'Song'], "ref" : 2},
    {"tag": "Method", "name" : "", "path": ['Live', 'Application', 'Application', 'View', 'remove_view_focus_changed_listener()']},
    {"tag": "Method", "name" : "Live.Application.Application.View.scroll_view()", "path": ['Live', 'Application', 'Application', 'View', 'scroll_view()']},
    {"tag": "Method", "name" : "Live.Application.Application.View.toggle_browse()", "path": ['Live', 'Application', 'Application', 'View', 'toggle_browse()']},
]
def make_references():
    dic = start_dic
    #  get class references
    for f_class in dic[0]:
        pass

def get_class(class_name):
    pass

def main():
    make_references()
    for element in start_dic:
        print(element['path'][0:-1])

if __name__ == "__main__":
    main()