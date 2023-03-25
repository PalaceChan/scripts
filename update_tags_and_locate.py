#!/usr/bin/python
import os
import shutil
import subprocess

root_dir = os.path.expanduser("~/rabbit/tagsAndLocates")

all_tag_paths = [
    "/usr/include/",
    "~/.emacs.d/elpa/",
    "~/development/helm-shell-history/",
]

all_loc_paths = []


def backup(path):
    old = f"{path}.old"
    older = f"{path}.older"
    oldest = f"{path}.oldest"
    if not os.path.exists(old):
        shutil.move(path, old)
    else:
        if not os.path.exists(older):
            shutil.move(old, older)
            shutil.move(path, old)
        else:
            if not os.path.exists(oldest):
                shutil.move(older, oldest)
                shutil.move(old, older)
                shutil.move(path, old)
            else:
                shutil.rmtree(oldest)
                shutil.move(older, oldest)
                shutil.move(old, older)
                shutil.move(path, old)


def do_tags(root_path):
    all_folders = " ".join(all_tag_paths)
    full_cmd = f"ctags -e --verbose --totals=yes --links=no --kinds-c++=+p --languages=c,c++,lisp --langmap=c++:+.I -R {all_folders} &> ctags.out"
    print(full_cmd)
    subprocess.check_call(full_cmd, shell=True, cwd=root_path)


def do_locate(root_path):
    i = 0
    for p in all_loc_paths:
        update_db_cmd = f"updatedb -l 0 -o {root_path}/{i}.db -U {p}"
        print(update_db_cmd)
        subprocess.check_call(update_db_cmd, shell=True, cwd=root_path)
        i = i + 1
    path_var = ":".join([f"{root_path}/{idx}.db" for idx in range(i)])
    emacs_cmd = f"locate %s -d {path_var} -e --regex %s"
    with open(f"{root_path/cmd.txt}", "w") as cmd_file:
        cmd_file.write(emacs_cmd + "\n")
    print(emacs_cmd)


if __name__ == "__main__":
    if os.path.exists(root_dir):
        backup(root_dir)
        os.mkdir(root_dir)

    if all_tag_paths:
        doTags(root_dir)
    if all_loc_paths:
        doLocate(root_dir)
