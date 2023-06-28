import tkinter


class SettingWin:
    parent_win = None

    def __init__(self, parent_win):
        self.parent_win = parent_win

    def show(self):
        frame = tkinter.Frame(self.parent_win, padx=20, pady=20)

        label1 = tkinter.Label(
            frame,
            text="API配置",
            font=("Arial", 14),
            fg="black",
            borderwidth=1,
            anchor="w"
        )
        label1.place(x=0, y=0, width=270, height=30)
        # 创建关闭按钮
        close_button = tkinter.Button(
            frame,
            text="X",
            fg="black",
            command=frame.destroy,
            width=1, height=50
        )
        close_button.place(x=270, y=0, width=30, height=30)  # 右上角对齐

        # # 创建画布
        # canvas = tkinter.Canvas(self.parent_win, width=400, height=300)
        # canvas.pack()
        #
        # # 绘制线条
        # canvas.create_line(50, 50, 350, 250, width=2, fill="blue")
        frame.place(x=330, y=0, width=330, height=400)
