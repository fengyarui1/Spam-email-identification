import hashlib
import tkinter as tk
from datetime import datetime
from tkinter.scrolledtext import ScrolledText


class CenterText(tk.PanedWindow):

    INPUT_NULL = -1
    INPUT_SAME = -2

    def __init__(self):
        super(CenterText,self).__init__()
        #水平排列
        self.config(orient=tk.HORIZONTAL)
        #初始化
        self.init_widgets()
        #预定义字体
        self.info_area.tag_configure("normal", font=("宋体", 10, "bold"), foreground="black")
        self.info_area.tag_configure("warn", font=("宋体", 10, "bold"), foreground="red")
        #邮件编码
        self.prev_hexdigest = ''


    #输入文本框和输出文本框
    def init_widgets(self):
        #输入
        self.mail_area=ScrolledText()
        self.info_area=tk.Text(wrap=tk.NONE)
        self.set_info_disable()
        #添加到窗口
        self.add(self.mail_area)
        self.add(self.info_area)

    #添加提示信息
    def add_info(self,text,font='normal'):
        #获取当前时间
        cur_time=datetime.now()
        cur_time=cur_time.strftime("%Y-%m-%d %H:%M:%S")
        message = f'{cur_time} {text}\n'
        self.set_info_enable()  # 点击按钮，让文本框可输入文字
        self.info_area.insert(tk.END, message, font)
        self.set_info_disable()#提示信息设置为不可输入文字

    # 获得邮件内容
    def get_mail(self):
        mail = self.mail_area.get("1.0", tk.END)  # 获得文本所有内容
        #判断邮件内容是否为空
        # print(f"mail 类型: {type(mail)}")
        # print(f"mail 内容: {repr(mail)}")  # 使用 repr() 显示原始内容，包括隐藏字符
        # print(f"mail 长度: {len(mail)}")
        if len(mail) == 1:
            return CenterText.INPUT_NULL

        #判断邮件内容是否相等
        hash=hashlib.sha256()
        hash.update(mail.encode())
        cur_encode=hash.hexdigest()#保存上次邮件的hash编码来判断
        #print(cur_encode)

        if cur_encode == self.prev_hexdigest:
            return CenterText.INPUT_SAME
        #缓存上次邮件内容
        self.prev_hexdigest=cur_encode
        #print(mail)
        return mail


    #文本框内可以输入
    def set_info_disable(self):
        self.info_area.config(state=tk.DISABLED)

    #文本框内不可输入
    def set_info_enable(self):
        self.info_area.config(state=tk.NORMAL)



if __name__ == '__main__':
    window=tk.Tk()
    window.geometry("800x500+200+200")

    text=CenterText()
    text.pack(fill="both",expand=True)

    button1=tk.Button(text='添加文本',command=lambda:text.add_info('测试'))
    button1.pack(side=tk.BOTTOM)

    button2 = tk.Button(text='获得文本', command=lambda: print(text.get_mail()))
    button2.pack(side=tk.BOTTOM)

    window.mainloop()