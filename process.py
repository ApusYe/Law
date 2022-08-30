#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
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

# 处理目录标题
def t1_proc(matched):
    h1_num = '- ' + matched.group('h1_num')
    return h1_num

def t2_proc(matched):
    h2_num = '\t- ' + matched.group('h2_num')
    return h2_num

def t3_proc(matched):
    h3_num = '\t\t- ' + matched.group('h3_num')
    return h3_num

def t4_proc(matched):
    h4_num = '\t\t\t- ' + matched.group('h4_num')
    return h4_num

   
# 计算标题层级的函数
def h_cal(list):
    a = 0
    b=[]
    for item in list:
         if re.match('第[零一二三四五六七八九十百千0-9]+分编', item):
             a=4
         elif re.match('第[零一二三四五六七八九十百千0-9]+编', item):
             a=3
         elif re.match('第[零一二三四五六七八九十百千0-9]+章', item):
             a=2
         elif re.match('[零一二三四五六七八九十百千0-9]+、', item):
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
    
    

s = '/Users/Ye/Downloads/监管规则适用指引——法律类第2号 律师事务所从事首次公开发行(FBM-CLI-4-5114001).txt'

with open(s , mode='r+') as filetxt, open(s.replace('txt','md'), mode='w') as new_filetext:
     lines=filetxt.readlines()
     toc_lvs=h_cal(lines)
     if_toc = False
     for line in lines:
         line = line.replace('　',' ') #全角空格转换为半角空格
         line = re.sub('(?P<period>。\s*)(?P<toc>第[零一二三四五六七八九十百千0-9]+(编|分编|章|节) [\u4e00-\u9fa5]+$)',toc_linebreak,line) # 标题行纠正
         if re.match('\s*目录',line):
             line=re.sub('\s*目\s*录', '# 目录', line, 1) # 目录作一级标题处理
             if_toc = True 
         if re.match('\s*第[零一二三四五六七八九十百千0-9]+条',line):
             line=re.sub('(?P<t_num>第[零一二三四五六七八九十百千0-9]+条)', t_proc, line, 1) # “第*条”处理
         # 下面是目录部分标题层级的处理
         if if_toc == True:
             if toc_lvs == 1:
                 if re.match('\s+[零一二三四五六七八九十百千0-9]+、',line):
                     line=re.sub('\s+(?P<h1_num>[零一二三四五六七八九十百千0-9]+、)', t1_proc, line, 1) # "*、"作一级标题处理
             elif toc_lvs == 2:
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+章',line):
                     line=re.sub('\s+(?P<h1_num>第[零一二三四五六七八九十百千0-9]+章)', t1_proc, line, 1) # "第*章"作一级标题处理
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+节',line):
                     line=re.sub('\s+(?P<h2_num>第[零一二三四五六七八九十百千0-9]+节)', t2_proc, line, 1) # "第*节"，作二级标题处理
             elif toc_lvs == 3:
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+编',line):
                     line=re.sub('\s+(?P<h1_num>第[零一二三四五六七八九十百千0-9]+编)', t1_proc, line, 1) # "第*编"作一级标题处理
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+章',line):
                     line=re.sub('\s+(?P<h2_num>第[零一二三四五六七八九十百千0-9]+章)', t2_proc, line, 1) # "第*章"，作二级标题处理
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+节',line):
                     line=re.sub('\s+(?P<h3_num>第[零一二三四五六七八九十百千0-9]+节)', t3_proc, line, 1) # "第*节"，作三级标题处理
             elif toc_lvs == 4:
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+编',line):
                     line=re.sub('\s+(?P<h1_num>第[零一二三四五六七八九十百千0-9]+编)', t1_proc, line, 1) # "第*编"作一级标题处理
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+分编',line):
                     line=re.sub('\s+(?P<h2_num>第[零一二三四五六七八九十百千0-9]+分编)', t2_proc, line, 1) # "第*编"作二级标题处理
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+章',line):
                     line=re.sub('\s+(?P<h3_num>第[零一二三四五六七八九十百千0-9]+章)', t3_proc, line, 1) # "第*章"，作三级标题处理
                 if re.match('\s+第[零一二三四五六七八九十百千0-9]+节',line):
                     line=re.sub('\s+(?P<h4_num>第[零一二三四五六七八九十百千0-9]+节)', t4_proc, line, 1) # "第*节"，作四级标题处理
         # 下面是正文部分标题的处理
         if toc_lvs != 0:
             if toc_lvs == 1:
                 if re.match('[零一二三四五六七八九十百千0-9]+、',line):
                     line=re.sub('(?P<h1_num>[零一二三四五六七八九十百千0-9]+、)', h1_proc, line, 1) # "*、"作一级标题处理
             elif toc_lvs == 2:
                 if re.match('第[零一二三四五六七八九十百千0-9]+章',line):
                     line=re.sub('(?P<h1_num>第[零一二三四五六七八九十百千0-9]+章)', h1_proc, line, 1) # "第*章"作一级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+节',line):
                     line=re.sub('(?P<h2_num>第[零一二三四五六七八九十百千0-9]+节)', h2_proc, line, 1) # "第*节"，作二级标题处理
             elif toc_lvs == 3:
                 if re.match('第[零一二三四五六七八九十百千0-9]+编',line):
                     line=re.sub('(?P<h1_num>第[零一二三四五六七八九十百千0-9]+编)', h1_proc, line, 1) # "第*编"作一级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+章',line):
                     line=re.sub('(?P<h2_num>第[零一二三四五六七八九十百千0-9]+章)', h2_proc, line, 1) # "第*章"，作二级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+节',line):
                     line=re.sub('(?P<h3_num>第[零一二三四五六七八九十百千0-9]+节)', h3_proc, line, 1) # "第*节"，作三级标题处理
             elif toc_lvs == 4:
                 if re.match('第[零一二三四五六七八九十百千0-9]+编',line):
                     line=re.sub('(?P<h1_num>第[零一二三四五六七八九十百千0-9]+编)', h1_proc, line, 1) # "第*编"作一级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+分编',line):
                     line=re.sub('(?P<h2_num>第[零一二三四五六七八九十百千0-9]+分编)', h2_proc, line, 1) # "第*编"作二级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+章',line):
                     line=re.sub('(?P<h3_num>第[零一二三四五六七八九十百千0-9]+章)', h3_proc, line, 1) # "第*章"，作三级标题处理
                 if re.match('第[零一二三四五六七八九十百千0-9]+节',line):
                     line=re.sub('(?P<h4_num>第[零一二三四五六七八九十百千0-9]+节)', h4_proc, line, 1) # "第*节"，作四级标题处理  
         if re.search('\t+-',line) == None:
             line= re.sub('^[\t ]+|[\t ]+$','',line) #去掉首尾多余的空格和制表符
         if re.search('\S',line):
             new_filetext.write(line)
         print(line)


print(toc_lvs,if_toc)         
print('finished')