import tkinter as tk
from tkinter import ttk


def on_select(event):
    selected_value = combobox.get()
    print("Selected:", selected_value)


root = tk.Tk()

# 创建一个下拉框
combobox = ttk.Combobox(root)
combobox['values'] = ('Option 1', 'Option 2', 'Option 3')  # 设置选项列表
combobox.bind('<<ComboboxSelected>>', on_select)  # 绑定选中事件的回调函数
combobox.pack()

root.mainloop()
