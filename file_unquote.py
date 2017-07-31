#!/usr/bin/env python3

from urllib.parse import unquote
import shutil
import sys

"""
fix the chinese named file downloaded via firefox/chromium can't be read.
example:
    $ ./file_unquote.py ElasticSearch++%E5%8F%AF%E6%89%A9%E5%B1%95%E7%9A%84%E5%BC%80%E6%BA%90%E5%BC%B9%E6%80%A7%E6%90%9C%E7%B4%A2%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88.pdf
    mv ElasticSearch++%E5%8F%AF%E6%89%A9%E5%B1%95%E7%9A%84%E5%BC%80%E6%BA%90%E5%BC%B9%E6%80%A7%E6%90%9C%E7%B4%A2%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88.pdf to ElasticSearch  可扩展的开源弹性搜索解决方案.pdf ? y
    $ ls
    ElasticSearch  可扩展的开源弹性搜索解决方案.pdf
"""

def getUnicodeName(name):
    return unquote(name).replace("+", " ")

if "__main__" == __name__:
    if len(sys.argv) == 1 :
        print("usage: {} filename ...".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    for f in sys.argv[1:]:
        nf = getUnicodeName(f)
        choice = input("mv {} to {} [y/N]? ".format(f, nf))
        if "y" == choice.lower() :
            shutil.move(f, nf)

