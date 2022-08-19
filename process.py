#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
import re
 
# “第*条”前后加上两个*号，并在前面加上一个换行
def t_proc(matched):
    t_num = '\n**'+ matched.group('t_num') +'**'
    return t_num


s = '/Users/Ye/Downloads/监管规则适用指引——法律类第2号 律师事务所从事首次公开发行(FBM-CLI-4-5114001).txt'

with open(s , mode='r+') as filetxt, open(s.replace('txt','md'), mode='w') as new_filetext:
     lines=filetxt.readlines()
     for line in lines:
         line=re.sub('(?P<t_num>第[零一二三四五六七八九十百千万1-9]+条)', t_proc, line, 1)
         new_filetext.write(line)
         print(line)

         
print('finished')


    