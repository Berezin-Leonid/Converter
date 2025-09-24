import zarr


def walk(group, prefix=""):
    keys = list(group.keys())
    for i, key in enumerate(keys):
        item = group[key]
        connector = "├── " if i < len(keys) - 1 else "└── "
        if isinstance(item, zarr.Group):
            print(prefix + connector + key + "/")
            extension = "│   " if i < len(keys) - 1 else "    "
            walk(item, prefix + extension)
        elif True:  # zarr.Array
            print(prefix + connector + f"{key} (array, shape={item.shape})")


def arrays_info(group, prefix=""):
    keys = list(group.keys())
    for i, key in enumerate(keys):
        item = group[key]
        connector = "├── " if i < len(keys) - 1 else "└── "
        if isinstance(item, zarr.Group):
            print(prefix + connector + key + "/")
            extension = "│   " if i < len(keys) - 1 else "    "
            arrays_info(item, prefix + extension)
        elif isinstance(item, zarr.Array):
            print(prefix + connector + f"{key} (array)")
            print(item.info)
            print("-" * 60)
    # Если напечаталась информация больше, чем о пяти массивах, остановка

def complect_info_group(group):
    print(22 * "=")
    print(f"Structure:")
    walk(group)
    print(22 * "=")
    print("Arrays info:")
    arrays_info(group)
    print(22 * "=")