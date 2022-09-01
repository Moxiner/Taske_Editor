from http.client import OK
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Task_Editor import Config , FileDir_Path
from Task_Editor import WriteFile



def NewTaskGUI(title):
    global Window
    global NewTask_name
    global NewTask_file
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
    OKNewTask_button.bind("<ButtonRelease-1>", QuitNewTask)
    CancelNewTask_button = ttk.Button(NewTask_fram3 , text="新建子任务" ,width=16)
    CancelNewTask_button.bind("<ButtonRelease-1>", Save_NewTask)


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

    
def QuitNewTask(*arg):
    Window.destroy()

def Save_NewTask(*arg):
    ConfigDate = Config["tasks"].append(NewTask_file.get())
    WriteFile(f"{FileDir_Path}/Config.json" , ConfigDate)
    data = {
        "name":NewTask_name.get,
        "tasks":[]
    }
    WriteFile(f"{FileDir_Path}/{NewTask_file}.json" , data)  
    Window.destroy()

def 打印(data):
    print(data)