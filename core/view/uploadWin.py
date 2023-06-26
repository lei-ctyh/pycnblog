import tkinter
import windnd
from tkinter import *


def dragged_files(files):
    """
    文件拖入窗口之后, 触发的回调函数
    :param files:
    :return:
    """
    for file in files:
        print(file.decode('utf-8'))


class UploadWin:
    """
    主窗体
    """
    window = None

    header = None

    body = None

    footer = None

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("markdown文件上传服务")
        self.window.geometry("660x408")
        self.window.resizable(False, False)
        self.add_header()
        self.add_body()

    def show(self):
        windnd.hook_dropfiles(self.window, func=dragged_files)
        self.window.mainloop()

    def add_header(self):
        frame = tkinter.Frame(self.window, padx=20, pady=20)
        label = tkinter.Label(
            frame,
            text="   请点击右下角设置按钮配置API后再使用，同时请遵守服务提供方上传规则。（点此查看帮助）",
            font=("Arial", 10),
            fg="#975a80",
            bg="#fff9e6",
            anchor="w")
        label.pack(fill="both", expand=True)
        '''
        x 和 y：控件的左上角在窗口中的 x 和 y 坐标位置。width 和 height：控件的宽度和高度。
        '''
        frame.place(x=0, y=0, width=660, height=100)

    def add_body(self):
        frame = tkinter.Frame(self.window, padx=20, pady=0)
        # 创建一个Canvas，设置其背景色为白色
        cv = Canvas(frame, bg='white')

        # 定义云朵的坐标和颜色
        cloud_coords = (50, 50, 200, 150)
        cloud_color = "#D3D3D3"  # 灰色
        # 绘制云朵
        cv.create_oval(cloud_coords, fill=cloud_color)
        cv.pack(fill="both", expand=True)

        frame.place(x=0, y=100, width=660, height=200)
