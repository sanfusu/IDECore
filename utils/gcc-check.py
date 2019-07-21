#!/usr/bin/python3
import json
import sys
import os
import argparse
from pathlib import Path


parser = argparse.ArgumentParser(description='check single c file accroding to the compile_commands.json')
parser.add_argument('--compdb', dest='compdb_file_name', 
        metavar='compile_commands.json', default='./compile_commands.json')
        
parser.add_argument('-f', dest='target_c_file')

args = parser.parse_args()

#def find_c_target(list):
    #for index,value in enumerate(list[1:]):
        #if Path(value).exists() and (not list[index-1].startswith('-')):
            #print(index,value)
            #list[index] = str(Path(value).resolve())

f = open(args.compdb_file_name, 'r')
obj = json.load(f)
for value in obj:
    if str(Path(value['directory'], value['file']).resolve()) == str(Path(args.target_c_file).resolve()):
        f.close()
        os.chdir(Path(args.compdb_file_name).resolve().parent)
        value['arguments'][-1] = str(Path(value['arguments'][-1]).resolve())
        print(value['arguments'])
        os.execvp('/usr/bin/gcc',value['arguments'])
