#!/opt/homebrew/bin/python3
# -*- coding: UTF-8 -*-

import os,sys,re

def trans(a):
    b = a.replace('中华人民共和国','')\
    .replace('最高人民法院','最高法')\
    .replace('最高人民检察院','最高检')
    b = re.sub('\(FBM-CLI\.\d{1}\.\d{7}\)','',b)
    return b 


filename = sys.argv[1]
os.rename(filename,trans(filename))