#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import shutil
 
try:
    shutil.rmtree(r"source\angora")
except Exception as e:
    print(e)
     
docfly = Docfly("angora", dst="source", 
    ignore=[
        "angora.zzz_manual_install.py",
    ]
)
docfly.fly()
