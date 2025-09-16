import random
import tkinter as tk


class StatusBar(tk.Frame):
    def __init__(self):
        super(StatusBar, self).__init__()
        # 设置控件属性
        self.config(borderwidth=0, bg='#bdc3c7')
        # 初始化子控件
        self.message = tk.Label(self, text=" 准备就绪", bg='#bdc3c7')
        self.message.pack(side=tk.LEFT)

    def set_message(self, txt):
        self.message['text'] = txt

if __name__ == '__main__':
    window = tk.Tk()
    window.geometry('800x500+300+300')

    sbar = StatusBar()
    sbar.pack(side=tk.BOTTOM, fill=tk.X)

    buttom=tk.Button(text='按钮',command=lambda :sbar.set_message('修改文字'))
    buttom.pack(side=tk.TOP)

    window.mainloop()