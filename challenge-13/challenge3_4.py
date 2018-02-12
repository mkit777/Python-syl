#!-*-coding:utf-8-*-
import re 
from datetime import datetime
def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                '(\d+.\d+.\d+.\d+)\s-\s-\s'
                '\[(.+)\]\s'
                '"GET\s(.+)\s\w+/.+"\s'
                '(\d+)\s'
                '(\d+)\s'
                '"(.+)"\s'
                '"(.+)"'
                )
        parsers = re.findall(pattern,logfile.read())
    return parsers

def main():
    logs = open_parser('/home/shiyanlou/Code/nginx.log')
    host_count={}
    url_count={}
    for log in logs:
        if '11/Jan/2017' in log[1]:
            host_count[log[0]] = host_count.get(log[0],0)+1
        if log[3] == '404':
            url_count[log[2]] = url_count.get(log[2],0)+1
    host_max = max(host_count.values())
    url_max = max(url_count.values())
    for k,v in host_count.items():
        if v==host_max:
            ip_dict={k:v}
            break
    for k,v in url_count.items():
        if v==url_max:
            url_dict = {k,v}
            break
    return ip_dict,url_dict

if __name__=='__main__':
    ip_dict,url_dict = main()
    print(ip_dict, url_dict)
