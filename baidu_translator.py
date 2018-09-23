#coding=utf-8
#author:Zhoubin
from tkinter import *                             # UI
import hashlib                                    # 哈希加密
import random                                     # 随机数
import getpass                                    # 用户名
import requests                                   # 网络请求
'''
程序功能：调用百度翻译API，实现在线翻译，外语(不限语种)译中文，中文译英语，支持单词、整句翻译
百度翻译官方文档: http://api.fanyi.baidu.com/api/trans/product/apidoc
'''
def getTransText(in_text):
    q = in_text
    print q
    fromLang = 'auto'                             # 翻译源语言=自动检测
    toLang1 = 'auto'                              # 译文语言 = 自动检测
    appid = '20180922000210913'                   # APP ID
    salt = random.randint(32768, 65536)           # 随机数
    secretKey = '6bmHfUxhfXkXFDqlWiim'            # 密钥
    sign = appid+q+str(salt)+secretKey            # 生成sign
    m1 = hashlib.md5(sign.encode('utf-8'))        # 计算签名sign,md5加密，UTF-8编码
    sign = m1.hexdigest()                         # 32位小写的md5

    myurl = '/api/trans/vip/translate'            # 拼接请求url
    myurl = myurl+'?appid='+appid+'&q='+q+'&from='+fromLang+'&to='+toLang1+'&salt='+str(salt)+'&sign='+sign
    url = "http://api.fanyi.baidu.com"+myurl

    url = url.encode('utf-8')
    res = requests.get(url)
    res = eval(res.text)
    result_text = res['trans_result'][0]['dst']
    return result_text.decode('unicode_escape').encode('utf-8') # 中文编码

user_name = getpass.getuser()
root = Tk()
root.title("百度翻译          欢迎您,{}!".format(user_name))
try:
    root.iconbitmap('baidu.ico')
except:
    pass
root.geometry('400x450+440+400')                   # UI长宽、坐标
root.resizable(width=True, height=True)            # 宽不可变, 高可变,默认为True
l = Label(root, text="(C) 周斌 保留所有权利", font=("Arial", 10), width=30)
l.pack(side=BOTTOM)
t = Text()
t.pack()
t.insert('1.0', "此处显示历史翻译内容\n")
var = StringVar()
e = Entry(root, textvariable = var)
var.set('此处显示最新翻译内容')
e.pack()

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.nameInput = Entry(self)
		self.nameInput.bind('<Key-Return>',self.hello)
		self.nameInput.pack()
		self.alertButton = Button(self, text='一键翻译', command=self.hello,width = 20,height = 2,bd = 2)
		self.alertButton.pack()

	def hello(self,event=None):
		in_text = self.nameInput.get() or '请输入需要翻译的内容'
		data=getTransText(in_text)
		var.set(data)
		t.insert('1.0', "-------------------------------------------------------\n")
		t.insert('1.0', "翻译: {}\n".format(data))
		t.insert('1.0', "原文: {}\n".format(in_text.encode('utf-8')))

app = Application()
app.mainloop()