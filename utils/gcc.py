#!/usr/bin/python3
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
f.close()


os.execvp('/usr/bin/gcc', sys.argv)
