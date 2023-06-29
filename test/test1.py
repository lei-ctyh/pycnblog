import tkinter as tk

# 创建顶级窗口
window = tk.Toplevel()

# 设置窗口样式
window.overrideredirect(True)  # 隐藏默认的窗口边框
window.attributes('-topmost', True)  # 窗口置顶

# 创建标题栏框架
title_bar = tk.Frame(window, bg='gray')
title_bar.pack(fill='x')

# 创建标题文本
title_label = tk.Label(title_bar, text='My Window Title', bg='gray', fg='white')
title_label.pack(side='left', padx=10, pady=5)

# 创建关闭按钮
close_button = tk.Button(title_bar, text='×', bg='red', fg='white', relief='flat', command=window.destroy)
close_button.pack(side='right', padx=10, pady=5)

# 添加其他窗口内容
# ...

# 设置窗口的大小和位置
window.geometry('400x300+100+100')

# 运行窗口的事件循环
window.mainloop()
