##dir_fuzz
参考ring04h多线程目录文件扫描

通过状态码判断文件是否存在

##用法

默认20个线程

默认字典/dics/dirs.txt

```
python dir_fuzz.py www.baidu.com php

python dir_fuzz.py www.baidu.com php  /dics/directory-list-1.0.txt

```
##修改配置

```
#配置
dic = './dics/dirs.txt'  #字典
timeout = 3       #超时时间
threads_num = 20  #线程
allow_redirects = False  #True允许重定向,Flase不允许
headers = {
		  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
	      'Referer' : 'http://www.baidu.com'
          'Mark': 'dirfuzz'
          }
cookies = {} #自定义cookies
```