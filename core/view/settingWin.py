import os.path
import tempfile
import tkinter
from tkinter import ttk

import yaml


def create_labeled(parent, label_text, posY):
    frame = tkinter.Frame(parent)
    label = tkinter.Label(frame,
                          text=label_text,
                          font=("Arial", 14),
                          fg="green",
                          borderwidth=1,
                          anchor="e",
                          width=7
                          )
    temp_label = tkinter.Label(frame,
                               text=" ",
                               font=("Arial", 14),
                               fg="green",
                               borderwidth=1,
                               anchor="w",
                               )
    label.pack(side="left")
    temp_label.pack(side="left")
    frame.place(x=0, y=posY, width=300, height=30)
    return frame


def create_labeled_entry(parent, label_text, posY, is_pwd=None):
    frame = create_labeled(parent, label_text, posY)
    entry = tkinter.Entry(frame, width=300, font=("Arial", 14), borderwidth=1, relief="raised", show=is_pwd)
    entry.pack(side="left")
    # # 当用户按下回车键时触发事件
    # entry.bind("<Return>", lambda event: on_entry_complete(event, entry, label_text))
    # # 当输入框失去焦点时触发事件
    # entry.bind("<FocusOut>", lambda event: on_entry_complete(event, entry, label_text))
    frame.place(x=0, y=posY, width=300, height=30)
    return entry


def create_labeled_combobox(parent, label_text, posY, tuples=None, current=0):
    frame = create_labeled(parent, label_text, posY)
    combobox = ttk.Combobox(frame, font=("Arial", 14), )
    if tuples is None:
        combobox['values'] = ()  # 将选项列表设置为空
    else:
        combobox['values'] = tuples  # 设置选项列表
        combobox.current(current)
    combobox.bind('<<ComboboxSelected>>', None)  # 绑定选中事件的回调函数
    combobox.pack()
    combobox.pack(side="left")
    frame.place(x=0, y=posY, width=300, height=30)
    return combobox


class SettingWin:
    parent_win = None
    """
    配置页相关组件
    按照前端展示顺序排列
    """
    component = []

    def __init__(self, parent_win):
        self.parent_win = parent_win

    def show(self):
        frame = tkinter.Frame(self.parent_win, padx=20, pady=20)

        title_label = tkinter.Label(
            frame,
            text="API配置",
            font=("Arial", 14),
            fg="black",
            borderwidth=1,
            anchor="w",
            relief="ridge"
        )
        title_label.place(x=0, y=0, width=270, height=30)
        # 创建关闭按钮
        close_button = tkinter.Button(
            frame,
            text="X",
            fg="black",
            command=lambda: self.on_entry_complete(frame),
            width=1, height=50
        )
        close_button.place(x=270, y=0, width=30, height=30)
        self.component.append({"blog_id", create_labeled_entry(frame, "账号", 50)})
        self.component.append({"blog_url", create_labeled_entry(frame, "链接", 90)})
        self.component.append({"password", create_labeled_entry(frame, "密码", 130, "*")})
        self.component.append({"categories", create_labeled_combobox(frame, "分类", 170)})
        self.component.append({"username", create_labeled_entry(frame, "用户名", 210)})
        self.component.append({"publish", create_labeled_combobox(frame, "是否发布", 250, ('发布', '未发布'), 1)})

        frame.place(x=330, y=0, width=330, height=400)

    def on_entry_complete(self, frame):
        temp_dir = os.path.join(tempfile.gettempdir(), 'pycnblog')
        # 检查目录是否存在
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        yaml_path = os.path.join(temp_dir, "config.yaml")
        # 检查文件是否存在
        if not os.path.exists(yaml_path):
            # 创建新文件
            with open(yaml_path, "w", encoding='utf-8') as file:
                file.write("# pycnblog 配置文件")

        config_yaml = {},
        for comp in self.component:
            for key in comp.keys():
                print(key)


        with open(yaml_path, "r", encoding="utf-8") as f:
            conf1 = yaml.load(f.read(), Loader=yaml.FullLoader)
        # 关闭配置窗口
        frame.destroy()
