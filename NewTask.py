import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def NewTaskGUI(title):
    Window = tk.Tk()
    Window.title(f"New Task - {title}")
    NewTask_fram1 = ttk.Frame(Window)
    NewTask_fram2 = ttk.Frame(Window)
    NewTask_fram3 = ttk.Frame(Window)
    NewTask_name_label = ttk.Label(NewTask_fram1 , text="任务名称")
    NewTask_name = ttk.Entry(NewTask_fram1 ,width=18)
    NewTask_file_label = ttk.Label(NewTask_fram2 , text="任务文件名称")
    NewTask_file = ttk.Entry(NewTask_fram2 ,width=18)
    OKNewTask_button = ttk.Button(NewTask_fram3 , text="确定新建" , width=16  )
    OKNewTask_button.bind("<<ComboboxSelected>>", )
    CancelNewTask_button = ttk.Button(NewTask_fram3 , text="新建子任务" ,width=16)
    CancelNewTask_button.bind("<<ComboboxSelected>>", )


    NewTask_fram1.pack( padx=10)
    NewTask_fram2.pack( padx=10)
    NewTask_fram3.pack( padx=10)
    NewTask_name_label.pack(side="left", padx=10, pady=10)
    NewTask_name.pack(side="left", padx=10, pady=10)
    NewTask_file_label.pack(side="left", padx=10, pady=10)
    NewTask_file.pack(side="left", padx=10, pady=10)
    OKNewTask_button.pack(side="left", padx=10, pady=10)
    CancelNewTask_button.pack(side="left", padx=10, pady=10)
    x_cordinate = int((Window.winfo_screenwidth() / 2) - (350 / 2))
    y_cordinate = int((Window.winfo_screenheight() / 2) - (180 / 2))
    Window.geometry("350x180+{}+{}".format(x_cordinate, y_cordinate-20))
    Window.tk.call("source", "azure.tcl")
    Window.tk.call("set_theme", "light")
    Window.mainloop()
