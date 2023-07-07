import os.path
import tempfile
import tkinter
from tkinter import ttk
from core.util.log_util import log
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
    combobox = ttk.Combobox(frame, font=("Arial", 14), state="readonly")
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
    frame = None
    """
    配置页相关组件
    按照前端展示顺序排列
    """
    component = []

    def __init__(self, parent_win):
        self.parent_win = parent_win
        self.frame = tkinter.Frame(self.parent_win, padx=20, pady=20)

        title_label = tkinter.Label(
            self.frame,
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
            self.frame,
            text="X",
            fg="black",
            command=lambda: self.on_entry_complete(),
            width=1, height=50
        )
        close_button.place(x=270, y=0, width=30, height=30)
        log.info("配置页标题以及按钮加载完毕")

        self.component.append({"blog_id": create_labeled_entry(self.frame, "账号", 50)})
        self.component.append({"blog_url": create_labeled_entry(self.frame, "链接", 90)})
        self.component.append({"password": create_labeled_entry(self.frame, "密码", 130, "*")})
        # self.component.append({"categories": create_labeled_combobox(self.frame, "分类", 170)})
        self.component.append({"username": create_labeled_entry(self.frame, "用户名", 170)})
        self.component.append({"publish": create_labeled_combobox(self.frame, "是否发布", 210, (True, False), 1)})
        log.info("参数设置输入框加载完毕")

        # 初始化选择框的值
        conf_path = os.path.join(tempfile.gettempdir(), 'pycnblog', "config.yaml")
        log.info("config.yaml 所在路径"+conf_path)

        if os.path.exists(conf_path):
            with open(conf_path, "r", encoding="utf-8") as f:
                conf_yaml = yaml.load(f.read(), Loader=yaml.FullLoader)

            for comp in self.component:
                for key in comp.keys():
                    if key in conf_yaml:
                        comp[key].delete(0, tkinter.END)  # 先清空输入框中的内容
                        if not conf_yaml[key] is None:
                            comp[key].insert(0, conf_yaml[key])  # 将新的值插入到输入框中
            log.info("文件存在,成功回写数据到输入框")

    def show(self):
        self.frame.place(x=330, y=0, width=330, height=400)

    def on_entry_complete(self):
        log.info("------------ 参数保存 ------------")
        temp_dir = os.path.join(tempfile.gettempdir(), 'pycnblog')
        # 检查目录是否存在
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        yaml_path = os.path.join(temp_dir, "config.yaml")
        # 检查文件是否存在
        if not os.path.exists(yaml_path):
            log.info("config.yaml文件不存在")
            # 创建新文件
            with open(yaml_path, "w", encoding='utf-8') as file:
                file.write("# pycnblog 配置文件")
            log.info("config.yaml创建成功")

        config_yaml = {}
        for comp in self.component:
            for key in comp.keys():
                config_yaml[key] = comp[key].get()

        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(yaml.dump(config_yaml))
        log.info("参数写入文件成功")
        # 关闭配置窗口 隐藏起来
        self.frame.place_forget()
