import sys
import tkinter as tk


class TopMenu(tk.Menu):

    def __init__(self, parent, predict_function):
        super().__init__(parent)
        self.predict_function = predict_function
        # 文件菜单
        self.file_menu()
        # 邮件菜单
        self.mail_menu()
        # 帮助菜单
        self.help_menu()

    def file_menu(self):
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label='打开')  # 打开按钮
        file_menu.add_separator()  # 分割符
        file_menu.add_command(label='退出', command=sys.exit)  # 退出按钮
        self.add_cascade(label='文件', menu=file_menu)  # 文件按钮

    def mail_menu(self):
        mail_menu = tk.Menu(self, tearoff=False)
        # command 函数由外部传递
        mail_menu.add_command(label='识别', command=self.predict_function)
        self.add_cascade(label='邮件', menu=mail_menu)

    def help_menu(self):
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='关于')
        self.add_cascade(label='帮助', menu=help_menu)


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry('800x500+300+300')

    def function():
        print('hello')

    menu = TopMenu(window, predict_function=function)
    window.config(menu=menu)
    window.mainloop()