# -*- coding: utf-8 -*-

"""
@Time        : 2020/12/15
@Author      : dosea
@File        : debug_main
@Description : 
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import re
from scrapy.cmdline import execute

if __name__ == '__main__':
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    # sys.exit(execute())
    execute(["scrapy", "crawl", "qsbk"])
