import requests
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# 初始化发件人的邮箱地址及其他信息
sender_email = 'sender@yeah.net'
sender_password = "sender's password"

# 初始化日志信息
logPath = './log.txt'

# 初始化请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}


### 抓取武汉大学网安学院新闻列表
def spyderGet_cseWhu():
    # 发送GET请求获取网页内容
    url = 'https://cse.whu.edu.cn/xwzx1/'  # 替换为你要爬取的网页的URL
    response = requests.get(url + 'tzgg.htm')
    response.encoding = 'utf-8'  # 设置编码方式为UTF-8

    # 解析网页内容
    html = etree.HTML(response.text)

    # 使用XPath定位目标元素
    elements = html.xpath('//*[@id="main-container"]/div/div/div/div[3]/div[3]/ul/li/a')

    # 初始化输出列表
    retList = []

    # 遍历每个目标元素
    for element in elements:
        # 提取链接和文本内容
        link = element.get('href')
        # text = element.text
        fullink = (url + link) if link.startswith("../") else link

        # 打印链接和文本内容
        # print("链接:", fullink)
        # 使用XPath定位<h3>标签并提取内容
        h3 = element.xpath('h3')
        if h3:
            h3_text = h3[0].text
            # print("<h3>标签内容:", h3_text)
        else:
            h3_text = "未获取到数据"

        # 使用XPath定位<span>标签并提取内容
        span = element.xpath('following-sibling::span[1]')
        if span:
            span_text = span[0].text
            # print("<span>标签内容:", span_text)
        else:
            span_text = "未获取到数据"

        retList.append([fullink, h3_text, span_text])
        # print()

    return retList


### 抓取武汉大学数学与统计学院新闻列表
def spyderGet_mathsWhu():
    import requests
    from lxml import etree

    # 发起 GET 请求获取网页内容
    url = "https://maths.whu.edu.cn/rcpy/yjsjy/yjszs/"
    response = requests.get(url+"xly.htm")
    response.encoding = 'utf-8'
    content = response.text

    # 使用 lxml 解析 HTML
    tree = etree.HTML(content)

    # 查找指定元素
    elements = tree.xpath('/html/body/div[2]/div/div[2]/div[2]/div/div[2]/ul/div/li/a')

    # 初始化输出列表
    retList=[]

    # 遍历指定元素并获取最靠近的 span 元素和链接
    for element in elements:
        # 使用 ../preceding-sibling::span[1] 获取最靠近的 span 元素
        span = element.xpath('../preceding-sibling::span[1]')
        if span:
            timetext = span[0].text
            # print(timetext)

        # 提取元素的文本内容
        header_text = element.text
        # print(header_text)

        # 提取元素的链接
        link = element.get("href")
        fullink = (url + link) if link.startswith("../") else link
        # print(fullink)

        retList.append([fullink, header_text, timetext])

    return retList


### 抓取武汉大学计算机学院新闻列表
def spyderGet_csWhu():
    # 发起 GET 请求获取网页内容
    url = "https://cs.whu.edu.cn/xwdt/"
    response = requests.get(url+"tzgg.htm")
    response.encoding = 'utf-8'
    content = response.text

    # 使用 lxml 解析 HTML
    tree = etree.HTML(content)

    # 查找所有符合条件的 li/a 元素
    elements = tree.xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li/a')

    # 初始化返回列表
    retList=[]

    # 遍历每个 li/a 元素
    for element in elements:
        # 获取 href 属性
        link = element.get("href")
        # print("Href:", link)
        fullink = (url + link) if link.startswith("../") else link

        # 查找 p 标签
        p_text = element.xpath('.//p/text()')
        if p_text:
            # print("P:", p_text[0].strip())
            p_text = p_text[0].strip()

        # 查找 span 标签
        span_text = element.xpath('.//span/text()')
        if span_text:
            # print("Span:", span_text[0].strip())
            span_text = span_text[0].strip()

        retList.append([fullink, p_text, span_text])
        # print("-----------------------")
    return retList


### 抓取华科网安学院新闻列表
def spyderGet_cseHust():
    # 发起 GET 请求获取网页内容
    url = "http://cse.hust.edu.cn/yjsjy/"
    response = requests.get(url+"tzgg.htm", headers=headers)
    response.encoding = 'utf-8'
    content = response.text

    # 使用 lxml 解析 HTML
    tree = etree.HTML(content)

    # 查找所有 li 元素
    li_elements = tree.xpath('/html/body/main/section/div/div/div/div[2]/div/div/div/ul/li')

    # 初始化返回列表
    retList=[]

    # 遍历每个 li 元素
    for li_element in li_elements:
        # 查找 div/b 元素
        b_elements = li_element.xpath('.//div/b')
        b_element = b_elements[0]
        b_text = b_element.text.strip()

        # 查找 div/span 元素
        span_elements = li_element.xpath('.//div/span')
        span_element = span_elements[0]
        span_text = span_element.text.strip()

        # 查找 div/b/a 元素
        a_elements = li_element.xpath('.//div/b/a')
        a_element = a_elements[0]
        a_text = a_element.text.strip()
        link = a_element.get("href")
        fullink = (url + link) if link.startswith("../") else link

        retList.append([fullink, a_text, span_text+'-'+b_text])
    return retList


### 发送邮件
def send_email(sender_email, sender_password, recipient_email, subject, message):
    # 创建MIME对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # 添加邮件内容
    msg.attach(MIMEText(message, 'plain'))

    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP_SSL('smtp.yeah.net', 465)  # 使用SSL连接，端口号为465
        server.login(sender_email, sender_password)

        # 发送邮件
        server.sendmail(sender_email, recipient_email, msg.as_string())
        writeLog("邮件发送成功", logPath)

    except Exception as e:
        writeLog("邮件发送失败:"+str(e), logPath)

    finally:
        # 关闭连接
        server.quit()


### 返回最新新闻列表
def getNews(ansList, historyList):
    retNews = [x for x in ansList if x not in historyList]
    if retNews:
        writeLog("发现新闻更新", logPath)
    return retNews


### 构造邮件内容
def getMailContents(news):
    return '\n------------------------' \
           '\n'.join('\n'.join(sublist) for sublist in news)


### 列表写入文件
def writeList(newList, filename):
    try:
        with open(filename, 'w') as file:
            # 清空文件内容
            file.truncate(0)

            # 将列表写入文件
            for sublist in newList:
                file.write('\n'.join(sublist))
                file.write('\n\n')
    except Exception as e:
        writeLog("写入文件出错:"+str(e), logPath)

    else:
        writeLog("列表写入文件成功", logPath)


### 列表读出文件
def readList(filename):
    retList = []
    try:
        with open(filename, 'r') as file:
            lines = file.read().split('\n\n')
            for line in lines:
                if line == '':
                    continue
                sublist = line.split('\n')
                retList.append(sublist)
    except FileNotFoundError:
        writeLog("文件不存在，返回空列表", logPath)
    return retList


### 写日志
def writeLog(contents, filename, flag=0):
    try:
        with open(filename, 'a+') as file:
            if flag == 1:
                file.truncate(0)
            file.write(time.ctime(time.time()) + ' - ' + contents + '\n')
    except Exception as e:
        print("写入日志出错:", str(e))
    else:
        print("日志写入成功")


### 读日志
def readLog(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except Exception as e:
        print("读取文件出错:", str(e))
    return content


### cse.whu爬虫主函数
def mainSpyder_csewhu(recipient_email):
    # 初始化
    historyListPath='./csewhu.txt'
    try:
        # 抓取新闻列表anslist
        ansList = spyderGet_cseWhu()
        # 读取旧新闻列表
        historyList = readList(historyListPath)
        # 获取最新的新闻列表news
        news = getNews(ansList, historyList)
        if news:
            # news列表转为邮件内容mailContents
            mailContents = getMailContents(news)
            # 获取邮件标题title
            title = 'cse.whu: ' + news[0][1] + ' ' + news[0][2]
            # 填写邮件标题及内容
            subject = title
            message = mailContents
            # 调用发送邮件函数
            send_email(sender_email, sender_password, recipient_email, subject, message)
            writeLog(title, logPath)
            # 更新historyList
            writeList(ansList, historyListPath)
    except Exception as e:
        writeLog(str(e), logPath)
        print(str(e))


### maths.whu爬虫主函数
def mainSpyder_mathswhu(recipient_email):
    # 初始化
    historyListPath='./mathswhu.txt'
    try:
        # 抓取新闻列表anslist
        ansList = spyderGet_mathsWhu()
        # 读取旧新闻列表
        historyList = readList(historyListPath)
        # 获取最新的新闻列表news
        news = getNews(ansList, historyList)
        if news:
            # news列表转为邮件内容mailContents
            mailContents = getMailContents(news)
            # 获取邮件标题title
            title = 'maths.whu: ' + news[0][1] + ' ' + news[0][2]
            # 填写邮件标题及内容
            subject = title
            message = mailContents
            # 调用发送邮件函数
            send_email(sender_email, sender_password, recipient_email, subject, message)
            writeLog(title, logPath)
            # 更新historyList
            writeList(ansList, historyListPath)
    except Exception as e:
        writeLog(str(e), logPath)
        print(str(e))


### cs.whu爬虫主函数
def mainSpyder_cswhu(recipient_email):
    # 初始化
    historyListPath='./cswhu.txt'
    try:
        # 抓取新闻列表anslist
        ansList = spyderGet_csWhu()
        # 读取旧新闻列表
        historyList = readList(historyListPath)
        # 获取最新的新闻列表news
        news = getNews(ansList, historyList)
        if news:
            # news列表转为邮件内容mailContents
            mailContents = getMailContents(news)
            # 获取邮件标题title
            title = 'cs.whu: ' + news[0][1] + ' ' + news[0][2]
            # 填写邮件标题及内容
            subject = title
            message = mailContents
            # 调用发送邮件函数
            send_email(sender_email, sender_password, recipient_email, subject, message)
            writeLog(title, logPath)
            # 更新historyList
            writeList(ansList, historyListPath)
    except Exception as e:
        writeLog(str(e), logPath)
        print(str(e))


### cse.hust爬虫主函数
def mainSpyder_csehust(recipient_email):
    # 初始化
    historyListPath='./csehust.txt'
    try:
        # 抓取新闻列表anslist
        ansList = spyderGet_cseHust()
        # 读取旧新闻列表
        historyList = readList(historyListPath)
        # 获取最新的新闻列表news
        news = getNews(ansList, historyList)
        if news:
            # news列表转为邮件内容mailContents
            mailContents = getMailContents(news)
            # 获取邮件标题title
            title = 'cse.hust: ' + news[0][1] + ' ' + news[0][2]
            # 填写邮件标题及内容
            subject = title
            message = mailContents
            # 调用发送邮件函数
            send_email(sender_email, sender_password, recipient_email, subject, message)
            writeLog(title, logPath)
            # 更新historyList
            writeList(ansList, historyListPath)
    except Exception as e:
        writeLog(str(e), logPath)
        print(str(e))


### 日志上传函数
def uploadLog(recipient_email):
    message = readLog(logPath)
    subject = "爬虫日志"
    send_email(sender_email, sender_password, recipient_email, subject, message)
