import urllib.request
import urllib.parse
import urllib.error
import os
from lxml import etree
import re
import socket


# 获取相应URL对应的html文件
# 参数：url（‘’）
# 返回值：异常（‘’），返回未解码的二进制字符串
def gethtml(url=''):
    try:
        re = urllib.request.urlopen(url, timeout=20)
    except urllib.error.HTTPError as e:
        print(e.code, e.reason)
        return ''
    except ValueError as e:
        print("Value Error!")
        return ''
    except UnicodeEncodeError as e:
        print("UnicodeEncodeError!")
        return ''
    except urllib.error.URLError as e:
        print("URLError:", e.reason)
    except socket.timeout as e:
        print("socket timeout:", url)
        return ''
    except:
        return ''
    # req=urllib.request.Request(url)
    # req.add_header('Accept-Encoding','deflate')
    # re=urllib.request.urlopen(req)
    return re.read()


# 建立文件存储路径并返回其路径
# 参数：路径path（默认当前路径），目标文件夹（target）
def buildpath(path='.', target='folder'):
    if path is '.':
        path = os.path.join(os.path.abspath(path), target)
    else:
        path = os.path.join(path, target)
        if not os.path.exists(path):
            os.mkdir(path)
            return path
    return path


def geturlbyre(url='', reg=''):
    data = gethtml(url)
    if data is '':
        return set()
    dataset = set()
    try:
        dataset = re.compile(reg).findall(data.decode('utf-8'))
    except UnicodeDecodeError as e:
        print('UnicodeDecodeError:', e)
    if not re.match('(http://|htpps://)', reg):
        for data in dataset:
            data = url + data
    return dataset


# temp=etree.HTML(data)
# urllist=temp.xpath(xpath)

def geturlbylxml(url='', lxmlpath='', abs=True):
    data = gethtml(url)
    if data is '':
        return set()
    temp = etree.HTML(data.decode('utf-8'))
    dataset = set(temp.xpath(lxmlpath))
    if not abs:
        for data in dataset:
            data += url
    print(dataset)
    return dataset


def savenews(path='.', prefix='', txtlist=[]):
    if txtlist is []:
        print("Yes")
        return
    n = 1
    path += ('\\' + prefix)
    for txt in txtlist:
        f = open(path + '_' + str(n) + '.txt', 'a+')
        for line in txt:
            try:
                f.write(line + '\n')
            except UnicodeEncodeError as e:
                print("Error file number:", n)
                print("UnicodeEncodeError:", e)
        f.close()
        n += 1


def get_txtlist(lists='', pattern=[]):
    if lists is '':
        return []
    txtlist = []
    for url in lists:
        txt = []
        print(url)
        data = gethtml(url)
        if data is '':
            continue
        temp = etree.HTML(data)
        txt += temp.xpath(pattern[0])
        txt += temp.xpath(pattern[1])
        if len(txt) is not 0:
            txtlist.append(txt)
    return txtlist


def main():
    # params={'url':"http://www.ce.cn/",
    # 		'ce_xpath':"http://finance\.ce\.cn/\S+\.shtml",
    # 		# ce_xpath='//div[@class="w_360 fl"]//ul[@class="triangle m_t10"]//li/a/@href'
    # 		'pattern':['//h1[@id="articleTitle"]/text()','//div[@class="TRS_Editor"]/p/text()']
    # }
    # params={'url':"https://wallstreetcn.com/news/china",
    # 		'ce_xpath':"//a[@class='home-news-item__main__title']/@href",
    # 		'pattern':['//div[@class="article__heading__title"]/text()','//div[@class="article__content"]//p/text()']
    # }
    params = {'url': "http://finance.sina.com.cn/",
              'ce_xpath': "http://finance.sina.com.cn/[^\s]+?\.shtml",
              'pattern': ['//h1[@id="artibodyTitle"]/text()', '//div[@id="artibody"]//p/text()']
              }
    # urllist=geturlbylxml(params['url'],params['ce_xpath'],False)
    # urllist=geturlbyre(params['url'],params['ce_xpath'])
    # newpath=buildpath(True,'c:\\users\\chencaijn\\desktop','2015News')
    # txtlist=get_txtlist(urllist,params['pattern'])
    month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # savenews(newpath,'20160101',txtlist)

    urllist = set()
    # for i in range(1,13):
    # 	j=1
    # 	while j<=month[i-1]:
    # 		str='%02d'%i+'{:0>2}'.format(j)
    # 		url='http://news.sina.com.cn/head/news2016'+str+'am.shtml'
    # 		print(url)
    # 		urllist=urllist|set(geturlbyre(url,params['ce_xpath']))
    # 		j+=1
    # txtlist=get_txtlist(urllist,params['pattern'])
    # savenews(newpath,'2016_',txtlist)
    for i in range(1, 13):
        j = 1
        while j <= month[i - 1]:
            str = '%02d' % i + '{:0>2}'.format(j)
            url = 'http://news.sina.com.cn/head/news2018' + str + 'am.shtml'
            # urllist=set(geturlbyre(url,params['ce_xpath']))# 可以保证一天之内的不重，但无法保证许多天的信息不重
            temp = set(geturlbyre(url, params['ce_xpath']))
            temp -= urllist & temp
            urllist = urllist | temp
            txtlist = get_txtlist(temp, params['pattern'])
            newpath = buildpath('/home/zry/PycharmProjects/python_news/news_test', '2018_' + str)
            savenews(newpath, '2018_' + str, txtlist)
            j += 1



if __name__ == '__main__':
    main()