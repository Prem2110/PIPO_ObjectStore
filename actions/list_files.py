from sap_os import list_objects
from datetime import datetime
from tabulate import tabulate


def readable_size(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def list_action(prefix=None):
    files = list_objects(prefix)

    if not files:
        print("No files found.")
        return

    table = []

    for obj in files:
        key = obj["key"]
        size = readable_size(obj["size"])
        ext = key.split(".")[-1] if "." in key else "-"
        uploaded = obj["last_modified"].astimezone().strftime("%Y-%m-%d %H:%M:%S")

        table.append([key, size, ext, uploaded])

    print("\nFiles in Object Store:\n")
    print(tabulate(
        table,
        headers=["File Name", "Size", "Type", "Uploaded Time"],
        tablefmt="grid",
        maxcolwidths=[50, None, None, None],
        stralign="left"
    ))


if __name__ == "__main__":
    list_action("demo/")
