#!/usr/bin/python
import os
import shutil
import subprocess

rootDir = os.path.expanduser("~/rabbit/tagsAndLocates")
rootDir = os.path.expanduser("~/rabbit/tagsAndLocates")

allTagPaths = [
    "/usr/include/",
    "~/.emacs.d/elpa/",
    "~/development/helm-shell-history/",
]

allLocPaths = [

]

def backup(path):
    old = f'{path}.old'
    older = f'{path}.older'
    oldest = f'{path}.oldest'
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

def doTags(rootPath):
    allFolders = ' '.join(allTagPaths)
    fullCmd = f'ctags -e --verbose --totals=yes --links=no --kinds-c++=+p --languages=c,c++,lisp --langmap=c++:+.I -R {allFolders} &> ctags.out'
    print(fullCmd)
    subprocess.check_call(fullCmd, shell = True, cwd = rootPath)

def doLocate(rootPath):
    i = 0
    for p in allLocPaths:
        updateDbCmd = f'updatedb -l 0 -o {rootPath}/{i}.db -U {p}'
        print(updateDbCmd)
        subprocess.check_call(updateDbCmd, shell = True, cwd = rootPath)
        i = i + 1
    pathVariable = ':'.join([f'{rootPath}/{idx}.db' for idx in range(i)])
    emacsCommand = f'locate %s -d {pathVariable} -e --regex %s'
    with open(f'{rootPath/cmd.txt}', 'w') as cmdFile:
        cmdFile.write(emacsCommand + '\n')
    print(emacsCommand)

if __name__ == '__main__':
    if os.path.exists(rootDir):
        backup(rootDir)
        os.mkdir(rootDir)

    if allTagPaths:
        doTags(rootDir)
    if allLocPaths:
        doLocate(rootDir)
