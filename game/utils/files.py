import shutil


def cat_files(out_path: str, *in_files: str):
    with open(out_path, 'wb') as out_file:
        for in_path in in_files:
            with open(in_path, 'rb') as in_file:
                shutil.copyfileobj(in_file, out_file)
