import os
import tkinter
import webbrowser

import windnd

from core.upload.upload import upload_file
from core.util.log_util import log
from core.view.settingWin import SettingWin


def dragged_files(files):
    log.info("------------ 拖入文件,开始上传文件 ------------")
    """
    文件拖入窗口之后, 触发的回调函数
    :param files:
    :return:
    """
    for file in files:
        upload_file(file.decode('GBK'))


def open_link(event):
    webbrowser.open("https://www.cnblogs.com/aaalei/p/17503371.html")


def resource_path(filename, level=2):
    current_dir = os.path.abspath(__file__)
    # 获取当前可执行文件的路径
    for num in range(0, level):
        current_dir = os.path.dirname(current_dir)
    # 构造资源文件的路径
    resource_file_path = os.path.join(current_dir, 'resources', filename)
    return resource_file_path


class UploadWin:
    """
    主窗体
    """
    window = None
    """
    上传图标必须以全局变量的形式存在, 
    不然PhotoImage长时间不使用该参数会被回收
    """
    body_image = None

    cogs_image = None

    setting_win = None

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("markdown文件上传服务")
        self.window.geometry("660x408")
        self.window.resizable(False, False)
        self.add_header()
        log.info("头部提示信息加载完毕")
        self.add_body()
        log.info("上传面板主题加载完毕")
        self.add_footer()
        log.info("版权声明, 参数设置按钮加载完毕")

    def show(self):
        self.window.mainloop()

    def open_setting_page(self):
        log.info("------------ 打开参数配置页面 ------------")
        if self.setting_win is None:
            self.setting_win = SettingWin(self.window)
        self.setting_win.show()

    def add_header(self):
        frame = tkinter.Frame(self.window, padx=20, pady=20)
        label1 = tkinter.Label(
            frame,
            text="  请点击右下角设置按钮配置API后再使用，同时请遵守服务提供方上传规则。",
            font=("Arial", 10),
            fg="#975a80",
            bg="#fff9e6",
            anchor="w"
        )
        label1.place(x=0, y=0, width=445, height=60)
        label2 = tkinter.Label(
            frame,
            text="（点此查看帮助）",
            font=("Arial", 10),
            fg="blue",
            bg="#fff9e6",
            anchor="w")
        label2.place(x=445, y=0, width=170, height=60)
        # 鼠标移动到按钮上时显示手型光标
        label2.config(cursor="hand2")
        label2.bind("<Button-1>", open_link)

        '''
        x 和 y：控件的左上角在窗口中的 x 和 y 坐标位置。width 和 height：控件的宽度和高度。
        '''
        frame.place(x=0, y=0, width=660, height=100)

    def add_body(self):
        self.body_image = tkinter.PhotoImage(file=resource_path('R.gif', 3))
        # 模拟外边距的frame
        frame = tkinter.Frame(self.window, padx=20, pady=0)
        # 拖拽区域
        label = tkinter.Label(
            frame, image=self.body_image)
        label.pack(fill="both", expand=True)
        frame.place(x=0, y=100, width=660, height=250)
        windnd.hook_dropfiles(frame, func=dragged_files)

    def add_footer(self):
        # 模拟外边距的frame
        frame = tkinter.Frame(self.window, padx=20, pady=20)
        # 版权声明label
        copyright_label = tkinter.Label(
            frame,
            text="    Copyright © 2023-2099 Powered by ZhangLei",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#888888"
        )
        copyright_label.place(x=0, y=0, width=590, height=30)

        # 参数设置按钮
        self.cogs_image = tkinter.PhotoImage(file=resource_path('Snipaste_2023-06-27_21-58-49.png', 3))
        setting_but = tkinter.Button(frame, text="设置", image=self.cogs_image, command=self.open_setting_page)
        setting_but.place(x=590, y=0, width=30, height=30)
        frame.place(x=0, y=350, width=660, height=100)
