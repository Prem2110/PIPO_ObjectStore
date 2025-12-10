from sap_os import list_objects
from collections import defaultdict

def build_tree(files):
    tree = lambda: defaultdict(tree)
    root = tree()

    for f in files:
        parts = f["key"].split("/")
        current = root
        for part in parts:
            current = current[part]

    return root

def print_tree(node, indent=""):
    keys = list(node.keys())
    for i, key in enumerate(keys):
        is_last = (i == len(keys) - 1)
        connector = "└── " if is_last else "├── "
        print(indent + connector + key)

        if node[key]:
            next_indent = indent + ("    " if is_last else "│   ")
            print_tree(node[key], next_indent)

def list_action(prefix=None):
    files = list_objects(prefix)

    if not files:
        print("No files found.")
        return

    tree = build_tree(files)

    print("\nDirectory tree:")
    print_tree(tree)


if __name__ == "__main__":
    list_action("demo/")
