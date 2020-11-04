import hashlib
import os
import re as regex
import zipfile
from os import listdir
from os.path import join
from pathlib import Path


def get_livery_files_hash_dict(livery_path):
    files = [f for f in listdir(livery_path) if os.path.isfile(join(livery_path, f)) and f != "description.lua"]
    file_hash_dict = {}
    for file in files:
        h = hashlib.sha256()
        with open(join(livery_path, file), "rb") as f:
            h.update(f.read())
        file_hash_dict[file.lower()] = h.hexdigest()
    return file_hash_dict


def execute(base_livery, prefix):
    working_dir = os.path.abspath(join(base_livery, '..'))

    print(os.path.basename(base_livery))

    liveries = [f for f in listdir(working_dir) if
                os.path.isdir(join(working_dir, f)) and f.startswith(prefix) and f != os.path.basename(base_livery)]

    print(liveries)

    base_livery_file_hash_dict = get_livery_files_hash_dict(base_livery)

    print(base_livery_file_hash_dict)

    for livery in liveries:
        zipf = zipfile.ZipFile(join(working_dir, livery.lower()) + ".zip", 'w', zipfile.ZIP_DEFLATED, compresslevel=9)
        print("looping through ", livery)
        livery_path = join(working_dir, livery)
        livery_description_lua_path = join(livery_path, "description.lua")
        livery_hash_dict = get_livery_files_hash_dict(livery_path)
        base_files = list(base_livery_file_hash_dict.keys())
        custom_files = []
        for (name, hash_) in livery_hash_dict.items():
            if name not in base_livery_file_hash_dict or base_livery_file_hash_dict[name] != hash_:
                custom_files.append(name)
                if name in base_files:
                    base_files.remove(name)
                zipf.write(join(livery_path, name), name)

        print(custom_files)
        print(base_files)
        with open(livery_description_lua_path, "rb") as f:
            contents = f.read()
            for base_file in base_files:
                contents = regex.sub(("\"(" + Path(base_file).stem + ")\"\\s*,\\s*false").encode(), (
                    "\"$LIVERIES/" + os.path.basename(base_livery) + "/" + Path(base_file).stem + "\"").encode(),
                                     contents, flags=regex.IGNORECASE)
            print(contents.decode())
        zipf.writestr("description.lua", contents.decode())
        zipf.close()
