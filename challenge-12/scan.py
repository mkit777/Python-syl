#!-*-coding:utf-8-*-
#!/usr/bin/env python3
import sys
import getopt
import socket
import re
def scan(ip,start,end=None):
    if end is None:
        end = start
    for port in range(start,end+1):
        if connecting(ip,port):
            print(port,'open')
        else:
            print(port,'closed')
def connecting(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.1)
    try:
        s.connect((ip,port))
        ret = True
    except:
        ret = False
        pass
    finally:
        s.close()
    return ret
def get_opt(args):
    options,args = getopt.getopt(sys.argv[1:],'',['host=','port='])
    for name,value in options:
        if name == '--host':
            if not re.match(r'\d+.\d+.\d+.\d+',value):
                print('Parameter Error')
                sys.exit()
            host = value
        elif name == '--port':
            port = value.split('-')
        else:
            print('Parameter Error')
            sys.exit()
    return host,map(int,port)

if __name__ == '__main__':
    host,port = get_opt(sys.argv)
    scan(host,*port)

