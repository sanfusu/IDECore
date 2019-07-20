#!/usr/bin/python3
"""
@brief
This script is used to create a compile_commands.json(ak, compile database)

@description
Rename this file to gcc, and export PATH=./:$PATH
so that make or other build system will find the gcc in curent directory.
And you may need to run chmod +x ./gcc to give a exec permission

@author:    sanfusu@foxmail.com
@date:      2019/7/20 10:42
"""
import json
import sys
import os
import fcntl
from pathlib import Path

compdb_file_name='./compile_commands.json'
new_compdb = {'arguments':[], 'directory':'', 'file':''}


def argv_to_dict():
    for i, v in enumerate(sys.argv):
        new_compdb['arguments'].append(v)
    p = Path(sys.argv[-1]).resolve()
    new_compdb['directory'] = str(p.parent)
    new_compdb['file'] = str(p.name)

sys.argv[0] = '/usr/bin/gcc'

if not Path(compdb_file_name).exists():
    Path(compdb_file_name).touch()
    f = open(compdb_file_name, 'r+')
    f.write('[]')
else:
    f = open(compdb_file_name, 'r+')

fcntl.flock(f, fcntl.LOCK_EX)
argv_to_dict()

pos = f.seek(0, 2)
f.seek(pos-1)
if pos > 2:
    f.write(',')
json.dump(new_compdb, f)
f.write(']')

f.flush()
os.fsync(f.fileno())
fcntl.flock(f, fcntl.LOCK_UN)
print(f.read())
f.close()


os.execvp('/usr/bin/gcc', sys.argv)
