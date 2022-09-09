#!/opt/homebrew/bin/python3
# -*- coding: UTF-8 -*-

from ast import Break, Continue
from email import contentmanager
import re

# 处理条
def t_proc(matched): 
    t_num = '\n**'+ matched.group('t_num') +'**'
    return t_num

# 处理正文标题
def h1_proc(matched):
    h1_num = '\n# ' + matched.group('h1_num')
    return h1_num

def h2_proc(matched):
    h2_num = '\n## ' + matched.group('h2_num')
    return h2_num

def h3_proc(matched):
    h3_num = '\n### ' + matched.group('h3_num')
    return h3_num

def h4_proc(matched):
    h4_num = '\n#### ' + matched.group('h4_num')
    return h4_num

   
# 计算标题层级的函数
def h_cal():
     a = 0
     b=[]
     for line in lines:
         if re.match('第[零一二三四五六七八九十百千0-9]+分编', line):
             a=4
         elif re.match('第[零一二三四五六七八九十百千0-9]+编', line):
             a=3
         elif re.match('第[零一二三四五六七八九十百千0-9]+章', line):
             a=2
         elif if_toc ==True and re.match('[零一二三四五六七八九十百千0-9]+、', line):
             a=1
         b.append(a)     
     return max(b)
             
# 纠正标题未独立成行的函数
def toc_linebreak(matched):
     if '分编' in matched.group('toc'):
         a = matched.group('period') + '\n\n## ' + matched.group('toc')
     elif '编' in matched.group('toc') :
         a = matched.group('period') + '\n\n# ' + matched.group('toc')
     elif '章' in matched.group('toc'):
        if toc_lvs == 4:
             a = matched.group('period') + '\n\n### ' + matched.group('toc')
        elif toc_lvs == 3:
             a = matched.group('period') + '\n\n## ' + matched.group('toc')
        elif toc_lvs == 2:
             a = matched.group('period') + '\n\n# ' + matched.group('toc')
     elif '节' in matched.group('toc'):
        if toc_lvs == 4:
             a = matched.group('period') + '\n\n#### ' + matched.group('toc')
        elif toc_lvs == 3:
             a = matched.group('period') + '\n\n### ' + matched.group('toc')
        elif toc_lvs == 2:
             a = matched.group('period') + '\n\n## ' + matched.group('toc')
     return a

# 纠正未独立成行的条文的函数
def t_linebreak(matched):
    return matched.group('period') + '\n\n**' + matched.group('t_num') + '**'

# 纠正未独立成行的项的函数
def x_linebreak(matched):
    return matched.group('period') + '\n' + matched.group('x_num')

# 判断是否有目录
def if_has_toc():
    for i in range(len(lines)):
        if re.match('\s*目\s*录\s*',lines[i]):
             lines[i]=re.sub('\s*目\s*录', '# 目录', lines[i], 1) # 目录作一级标题处理
             return True
    return False



    

s = '/Users/Ye/Downloads/监管规则适用指引——法律类第2号 律师事务所从事首次公开发行(FBM-CLI-4-5114001).txt'

with open(s , mode='r+') as filetxt, open(s.replace('txt','md'), mode='w') as new_filetext:
     lines=filetxt.readlines()
     lines1 = []
     for line in lines: # 删除空白行
         if re.search('\S',line):
             lines1.append(line)
     lines = lines1      
     for i in range(len(lines)):
         lines[i] = lines[i].replace('　',' ') #全角空格转换为半角空格，否则会出现正文标题无法被Markdown阅读器识别的问题
         lines[i]= re.sub('^[\t ]+|[\t ]+$','',lines[i]) #去掉首尾多余的空格和制表符
     if_toc = if_h_toc = if_has_toc()
     toc_lvs=h_cal()
     a = 0 #初始赋值，变量a用于判断本行是否为目录行，若是则a=1
     first_toc = 'This file has no directory！（此文件无目录！）' # 初始赋值，为了保证法条中无内容能与此匹配
     for i in range(len(lines)):
         # 以下为未换行纠正
         lines[i] = re.sub('(?P<period>。\s*)(?P<toc>第[零一二三四五六七八九十百千0-9]+(编|分编|章|节) [\u4e00-\u9fa5]+)',toc_linebreak,lines[i]) # 纠正正文内容中条与标题行之间未换行的问题
         lines[i] = re.sub('(?P<period>。\s*)(?P<t_num>第[零一二三四五六七八九十百千0-9]+条(\s*【[\u4e00-\u9fa5]+】)?)', t_linebreak ,lines[i]) # 纠正正文内容中条与条之间未换行的问题
         if toc_lvs == 0:
             lines[i] = re.sub('(?P<period>。\s*)(?P<t_num>[零一二三四五六七八九十百千0-9]+、)', t_linebreak ,lines[i]) # 纠正正文内容中条与条之间未换行的问题
         lines[i] = re.sub('(?P<period>；\s*)(?P<x_num>（[零一二三四五六七八九十百千0-9]+）\s*[\u4e00-\u9fa5]+)', x_linebreak ,lines[i]) # 纠正正文内容中项与项之间未换行的问题
         lines[i] = re.sub('(?P<period>：\s*)(?P<x_num>（[零一二三四五六七八九十百千0-9]+）\s*[\u4e00-\u9fa5]+)', x_linebreak ,lines[i]) # 纠正正文内容中项与项之间未换行的问题
         if re.match('第[零一二三四五六七八九十百千0-9]+条',lines[i]): 
             lines[i]=re.sub('(?P<t_num>第[零一二三四五六七八九十百千0-9]+条(\s*【[\u4e00-\u9fa5]+】)?)', t_proc, lines[i], 1) # “第*条”处理
         if re.match('[零一二三四五六七八九十百千0-9]+、\s*[\u4e00-\u9fa5]+',lines[i]) and toc_lvs == 0: 
             lines[i]=re.sub('(?P<t_num>[零一二三四五六七八九十百千0-9]+、)', t_proc, lines[i], 1) # “第*条”处理
         # 以下为对标题行的处理
         # 当存在目录时需要区分位置，目录及以上部分标题行不做处理
         if if_toc == True: 
             if a == 0 :
                 if '# 目录' in lines[i]:
                     a = 1
                 elif first_toc.replace('\n','') in lines[i] or lines[i].replace('\n','') in first_toc: # 此时进入正文第一行
                     lines[i]=re.sub('(?P<h1_num>第 *一 *[\u4e00-\u9fa5]|一 *、 *[\u4e00-\u9fa5])', h1_proc, lines[i], 1) # 正文第一行作一级标题处理
                     if_toc = False
             elif a == 1 :
                 first_toc = lines[i]
                 a = 0
                 
         # 不存在目录，或已脱离目录进入正文部分
         elif if_toc == False:
             if toc_lvs == 1:
                 if re.match('[零一二三四五六七八九十百千0-9]+、',lines[i]):
                     lines[i]=re.sub('(?P<h1_num>[零一二三四五六七八九十百千0-9]+、)', h1_proc, lines[i], 1) # "*、"作一级标题处理
             elif toc_lvs == 2:
                 if re.match('第[零一二三四五六七八九十百千0-9]+章',lines[i]):
                     lines[i]=re.sub('(?P<h1_num>第[零一二三四五六七八九十百千0-9]+章)', h1_proc, lines[i], 1) # "第*章"作一级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+节',lines[i]):
                     lines[i]=re.sub('(?P<h2_num>第[零一二三四五六七八九十百千0-9]+节)', h2_proc, lines[i], 1) # "第*节"，作二级标题处理
             elif toc_lvs == 3:
                 if re.match('第[零一二三四五六七八九十百千0-9]+编',lines[i]):
                     lines[i]=re.sub('(?P<h1_num>第[零一二三四五六七八九十百千0-9]+编)', h1_proc, lines[i], 1) # "第*编"作一级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+章',lines[i]):
                     lines[i]=re.sub('(?P<h2_num>第[零一二三四五六七八九十百千0-9]+章)', h2_proc, lines[i], 1) # "第*章"，作二级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+节',lines[i]):
                     lines[i]=re.sub('(?P<h3_num>第[零一二三四五六七八九十百千0-9]+节)', h3_proc, lines[i], 1) # "第*节"，作三级标题处理
             elif toc_lvs == 4:
                 if re.match('第[零一二三四五六七八九十百千0-9]+编',lines[i]):
                     lines[i]=re.sub('(?P<h1_num>第[零一二三四五六七八九十百千0-9]+编)', h1_proc, lines[i], 1) # "第*编"作一级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+分编',lines[i]):
                     lines[i]=re.sub('(?P<h2_num>第[零一二三四五六七八九十百千0-9]+分编)', h2_proc, lines[i], 1) # "第*分编"作二级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+章',lines[i]):
                     lines[i]=re.sub('(?P<h3_num>第[零一二三四五六七八九十百千0-9]+章)', h3_proc, lines[i], 1) # "第*章"，作三级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+节',lines[i]):
                     lines[i]=re.sub('(?P<h4_num>第[零一二三四五六七八九十百千0-9]+节)', h4_proc, lines[i], 1) # "第*节"，作四级标题处理          
                
         new_filetext.write(lines[i])

print('是否存在目录',if_h_toc,'\n目录部分标题行首行：',first_toc,'\n标题层级：',toc_lvs)         
print('finished') 