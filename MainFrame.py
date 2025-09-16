import tkinter as tk
from TopMenu import TopMenu
from CenterText import CenterText
from StatusBar import StatusBar
from RecognizerMail import RecognizerMail

class MainFrame(tk.Tk):

    def __init__(self):
        #初始化父类
        super().__init__()
        #高宽
        self.window_w,self.window_h = 900,500
        #初始化位置
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()
        #主窗口在屏幕正中间
        start_x, start_y = int(screen_w / 2 - self.window_w / 2), int(screen_h / 2 - self.window_h / 2)
        # 设置屏幕尺寸以及初始位置
        self.geometry(f'{self.window_w}x{self.window_h}+{start_x}+{start_y}')
        #标题
        self.title('垃圾邮件识别器')
        #初始化其他控件
        self.init_widgets()
        #初始化算法对象
        self.RecognizerMail = RecognizerMail()

    def init_widgets(self):
        #初始化头部
        self.menu = TopMenu(parent=self, predict_function=self.on_menu_predict)
        self.config(menu=self.menu)
        #初始化文本框
        self.text=CenterText()
        self.text.pack(fill=tk.BOTH, expand=True)
        #初始化状态栏
        self.sbar=StatusBar()
        self.sbar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_menu_predict(self):
        #1.获得文件内容
        email=self.text.get_mail()
        if email==CenterText.INPUT_NULL:
            self.text.add_info('邮件内容为空！',font='warn')
            return

        if email==CenterText.INPUT_SAME:
            self.text.add_info('邮件内容重复！', font='warn')
            return

        #2.算法模型预测
        self.sbar.set_message('邮件正在预测...')
        labels=self.RecognizerMail.predict([email])
        #3.输出预测结果
        self.text.add_info(f'预测结果：{labels[0]}',font='normal')
        self.sbar.set_message('邮件预测完毕...')


    def show(self):
        self.mainloop()
