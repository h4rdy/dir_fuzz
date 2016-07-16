#!/usr/bin/env python
# coding: utf-8
import threading
import Queue
import sys
import lib.requests as requests
from lib.termcolor import colored

#配置
dic = './dics/dirs.txt'  #字典
timeout = 3       #超时时间
threads_num = 50  #线程
allow_redirects = False  #True允许重定向,Flase不允许
dirqueue = Queue.Queue()
mutex = threading.Lock()
headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
          'Referer' : 'http://www.baidu.com',
          'Mark': 'dirfuzz'
          }
cookies = {} #自定义cookies

class Fuzz(threading.Thread):

    def __init__(self,dirqueue):
        threading.Thread.__init__(self)
        self.dirqueue = dirqueue

    def fuzz_start(self,url):
        return requests.get(url, cookies=cookies, headers=headers, stream=True, timeout=timeout, allow_redirects=allow_redirects)

    def run(self):
        while self.dirqueue.qsize() > 0:
            try:
                url = self.dirqueue.get_nowait()
                req = self.fuzz_start(url)
                if req.status_code == requests.codes.ok:
                    mutex.acquire()
                    print colored('[%s]:','green')% req.status_code,url
                    mutex.release()
                    dir_exists.append(url)
                else:
                    mutex.acquire()
                    print colored('[%s]:','red')% req.status_code,url
                    mutex.release()
            except:
                pass
                
def dir_fuzz(domain, file_type, dic):
    if not domain.startswith('http://'):
        domain = 'http://%s' % domain
    use_dic = open(dic,'r')
    global dir_exists
    dir_exists = []
    for dic_line in use_dic.readlines():
        line = '%s/%s'%(domain,dic_line.strip().replace('%EXT%', file_type))
        dirqueue.put(line)
    use_dic.close()
    threadList = []
    for i in range (threads_num):
        threadList.append(Fuzz(dirqueue))
    for t in threadList:
        t.start()
    for t in threadList:
        t.join()
    print ('-'*50)
    for url in dir_exists:
        print colored('%s','yellow')% url

if __name__ == "__main__":
    if len(sys.argv) == 3:
        dir_fuzz(sys.argv[1], sys.argv[2], dic)
    elif len(sys.argv) == 4:
        dir_fuzz(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print ("usage: %s www.baidu.com php" % sys.argv[0])