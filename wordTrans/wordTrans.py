#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import re ,sys ,os 
def read():
    file1 = open(filepath,'r',encoding='GBK',errors="ignore")
    content = file1.readlines()
    file1.close()
    # 以下操作为去除doc文件头，避免“邢\x11唷”乱码
    del content[0:2]
    line1 = content.pop(0)
    line1 = re.sub('.+<html><body>','<html><body>', line1 ,1)
    content.insert(0,line1)
    return content

def write(content):
    file2 = open(filepath,'w',encoding='utf-8', errors="ignore")
    file2.writelines(content)
    file2.close()
    
def rename(content):
    for line in content:
        matchObj = re.search('（\d{4}）[\u4e00-\u9fa5]{1,3}\d{0,4}[\u4e00-\u9fa5]+\d+号',line)
        if matchObj:
            case_number = matchObj.group()
            break
    else:
        case_number = ''
    os.rename(filepath,filepath.replace('.doc','【%s】.doc' % (case_number)))
            

filepath = '/Users/Ye/Downloads/南雨辰王鑫桐侵犯公民个人信息一审刑事判决书.doc'

file_content = read()
write(file_content)
rename(file_content)
