# 导入模块
from email import message
from email.message import Message
from tkinter import END
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import time
import tkinter.messagebox 
from typing import Any
import json
import random
import threading



# 创建窗口
Tasktitle = None
ID = None
IsTips = True
Window = tk.Tk()
Window.title(f"Task Editor - {Tasktitle}")
# Window.resizable(0,0)

# 数据处理函数
def thread():
    global tips
    tips = ReadFile("tips.json")
    t = threading.Thread(target = tipstext )
    t.setDaemon(True)
    t.start()
    

def  tipstext():
    global IsTips
    while True:
        if IsTips:
            tip = tips[random.randint(0,len(tips)-1)]
            time.sleep(10)
            Help_.config(text=tip)
        else:
            time.sleep(10)

def HelpLobel(content):
    Help_.config(text=content)


def ReadFile(path) :
    '''读取文件内容'''
    file = open(path , mode="r" , encoding='utf-8')
    date = file.read()
    file.close()
    return json.loads(date)

def WriteFile(path:str , date:str):
    '''写入文件'''
    if date == None:
        tkinter.messagebox.showerror(title="致命错误" , message="写入值为空，已取消本次写入！")
    else:
        file = open(path , mode="w" , encoding='utf-8')
        date = json.dumps(date, indent = 4, ensure_ascii= False)
        file.write(date)
        file.close()
        print(date)    
def JudgeMoneyType():
    '''判断经济系统
    :return <bool> -True:LLMoney -False:SCoreboard'''
    if Config["currency"] == "LLMoney":
        return True
    else:
        return False

def DelectEnrty(Entry):
    '''删除文本控件原始值
    :Entry <Entry> -文本控件'''
    Entry.delete(0 , "end")


def Update_treevive(treevive , date , column):
    """更新 Treevive控件数据
    :treevive <Treevive> 树目录控件
    :date <List> 更新内容
    :columm <List> 树目录表头
    """
    x = treevive.get_children()
    for item in x:
        treevive.delete(item)
    treelist = []
    columnlist = []
    for item  in date:
        for col in column :
            try: 
                columnlist.append(item[col])
            except:
                if col == "count":
                    try:
                        columnlist.append(item["unit"])
                    except:
                        columnlist.append("---")
                elif col == "name":
                    columnlist.append(item["cmd"])
                elif col == "object":
                    columnlist.append("---")
        columnlist = tuple(columnlist)        
        treelist.append(columnlist)
        columnlist = []
    for item in treelist:
        treevive.insert("",END,values=item)
# 控件事件
def NewFile():
    pass

def ImportFile():
    '''导入文件地址的操作'''
    global FileDir_Path
    FileDir_Path = filedialog.askdirectory()
    ReadConfig()


def ReadConfig():
    global Config
    Config = ReadFile(f'{FileDir_Path}/config.json')
    DelectEnrty(Config_verson)
    DelectEnrty(Config_lang)
    DelectEnrty(Config_money)
    DelectEnrty(Config_daily)
    SelectMainTask.config(values= Config["tasks"])
    Config_verson.insert("" , Config["version"])
    Config_lang.insert("end" , Config["lang"])
    if JudgeMoneyType() :
        Config_money.insert("end" , "LLMoney")
    else:
        Config_money.insert('end' , Config["scoreboard"])
    Config_daily.insert("end" , Config["daily"])
    Window.title(f"Task Editor - {FileDir_Path}")
    Help_.config(text="导入成功")
    

# 更新任务列表
def Down_SelecMainTask(*arg):
    global Tasks
    taskfile = SelectMainTask.get()
    Tasks = ReadFile(f'{FileDir_Path}/{taskfile}.json')
    DelectEnrty(MainTask_name)
    MainTask_name.insert("end" , Tasks["name"])
    Update_treevive(Task_Treevive , Tasks["tasks"] , ["id" ,"name"]) 
    Help_.config(text="任务已同步")

def Down_Task_treevive(*arg):
    global Task
    global Task_ID 
    if (Task_Treevive.selection()) == ():
        return False
    Task = {}

    DelectEnrty(TaskConfig_id)
    DelectEnrty(TaskConfig_name)
    DelectEnrty(TaskConfig_front)

    for item in Task_Treevive.selection():
        id = Task_Treevive.item(item,"values")[0]
    for item in Tasks["tasks"]:
        if item["id"] == id:
            Task = item
            Task_ID = item["id"]

    TaskConfig_id.insert("end" ,Task["id"])
    TaskConfig_name.insert("end" ,Task["name"])
    TaskConfig_front.insert("end" , "".join(Task["requirements"]))
    Update_treevive(TaskEdit_conditions_treeview , Task["conditions"] ,["name" ,"object" , "count" , "type"])
    Update_treevive(TaskEdit_rewards_treeview , Task["rewards"] ,["name" ,"object" , "count" , "type"])
    Help_.config(text="任务导入成功")

def Down_TaskEdit_conditions_treeview(*arg):
    global Task_conditions
    global Task_conditions_ID

    for item in TaskEdit_conditions_treeview.selection():
        name = TaskEdit_conditions_treeview.item(item,"values")[0]
        _object = TaskEdit_conditions_treeview.item(item,"values")[1]
        count = TaskEdit_conditions_treeview.item(item,"values")[2]
        type = TaskEdit_conditions_treeview.item(item,"values")[3]
    for item in Task["conditions"]:
        if item["name"] == name:
            if item["object"] == _object:
                if item["count"] == int(count):
                    if item["type"] == type:
                        Task_conditions = item
                        Task_conditions_ID = item["id"]
                        break
    DelectEnrty(TaskEdit_conditions_name)
    DelectEnrty(TaskEdit_conditions_object)
    DelectEnrty(TaskEdit_conditions_aux)
    DelectEnrty(TaskEdit_conditions_count)
    DelectEnrty(TaskEdit_conditions_type)
    TaskEdit_conditions_aux.config(state="normal")

    TaskEdit_conditions_name.insert("end" ,Task_conditions["name"])
    TaskEdit_conditions_object.insert("end" ,Task_conditions["object"])
    TaskEdit_conditions_count.insert("end" ,Task_conditions["count"])
    try:
        TaskEdit_conditions_aux.insert("end" ,Task_conditions["aux"])
    except:
        TaskEdit_conditions_aux.config(state="disable")
    TaskEdit_conditions_type.insert("end" ,Task_conditions["type"])

def Down_TaskEdit_rewoards_treeview(*arg):
    '''
    按下 任务奖励树状图 时刷新 任务奖励输入区数值
    '''
    global Task_rewards
    global Task_rewards_ID
    for item in TaskEdit_rewards_treeview.selection():
        name = TaskEdit_rewards_treeview.item(item,"values")[0]
        _object = TaskEdit_rewards_treeview.item(item,"values")[1]
        count = TaskEdit_rewards_treeview.item(item,"values")[2]
        type = TaskEdit_rewards_treeview.item(item,"values")[3]
    for item in Task["rewards"]:
        i = i + 1 
        if item["type"] == "command":
            if item["cmd"] == name:
                Task_rewards = item
                break
        elif item["type"] == "item":
            if item["name"] == name:
                if item["object"] == _object:
                    if item["count"] == int(count):
                        Task_rewards = item
                        break
        elif item["type"] == "money":
            if item["name"] == name:
                if item["count"] == int(count):
                    Task_rewards = item
                    Task_rewards_ID = i

                    break

    DelectEnrty(TaskEdit_rewards_name)
    DelectEnrty(TaskEdit_rewards_object)
    DelectEnrty(TaskEdit_rewards_aux)
    DelectEnrty(TaskEdit_rewards_lore)
    DelectEnrty(TaskEdit_rewards_ench)
    DelectEnrty(TaskEdit_rewards_count)
    DelectEnrty(TaskEdit_rewards_type)
    TaskEdit_rewards_object.config(state="normal")
    TaskEdit_rewards_object_label.config(text="目标对象")
    TaskEdit_rewards_count.config(state="normal")
    TaskEdit_rewards_aux.config(state="normal")
    TaskEdit_rewards_ench.config(state="normal")
    TaskEdit_rewards_lore.config(state="normal")
    if Task_rewards["type"] == "command":
        TaskEdit_rewards_name_label.config(text="指令内容")
        TaskEdit_rewards_name.insert("end" , Task_rewards["cmd"])
        TaskEdit_rewards_type.insert("end" , Task_rewards["type"])

        TaskEdit_rewards_object.config(state="disable")
        TaskEdit_rewards_count.config(state="disable")
        TaskEdit_rewards_aux.config(state="disable")
        TaskEdit_rewards_ench.config(state="disable")
        TaskEdit_rewards_lore.config(state="disable")
    elif Task_rewards["type"] == "item":
        TaskEdit_rewards_name_label.config(text="物品名称")
        TaskEdit_rewards_name.insert("end" , Task_rewards["name"])
        TaskEdit_rewards_object.insert("end" , Task_rewards["object"])
        TaskEdit_rewards_count.insert("end" , Task_rewards["count"])
        TaskEdit_rewards_aux.insert("end" , Task_rewards["aux"])
        TaskEdit_rewards_ench.insert("end" , Task_rewards["ench"])
        TaskEdit_rewards_lore.insert("end" , Task_rewards["lore"])
        TaskEdit_rewards_type.insert("end" , Task_rewards["type"])
    elif Task_rewards["type"] == "money":
        TaskEdit_rewards_name_label.config(text="货币名称")
        TaskEdit_rewards_name.insert("end" , Task_rewards["name"])
        TaskEdit_rewards_object_label.config(text="货币单位")
        TaskEdit_rewards_object.insert("end" , Task_rewards["unit"])
        TaskEdit_rewards_count.insert("end" , Task_rewards["count"])
        TaskEdit_rewards_type.insert("end" , Task_rewards["type"])
        TaskEdit_rewards_aux.config(state="disable")
        TaskEdit_rewards_ench.config(state="disable")
        TaskEdit_rewards_lore.config(state="disable")
        

def Save_ConfigEdit(*arg):
    try:
        Config["version"] = Config_verson.get()
        Config["lang"] = Config_lang.get()
        if Config_money.get() == "LLMoney":
            Config["currency"] = "LLMoney"
        else:
            Config["currency"] = "scoreboard"
        Config["scoreboard"] = Config_money.get()
        Config["daily"] = Config_daily.get()
        WriteFile(f"{FileDir_Path}/Config.json" , Config)
        ReadConfig()
        Help_.config(text="配置保存成功")
    except NameError as e:
            Help_.config(text="请先导入工程文件夹 ")

        


    
def OutportFile():
    pass
def ReOutportFile():
    pass

def NewTask():
    pass
def EditTask():
    pass
def DelTask():
    pass
def DailyTask():
    pass
def MainTask():
    pass

def Help():
    pass
def Exit():
    pass


Help_ = ttk.Label(Window)
ttk.Label(text="")
MenuBar = tk.Menu(Window)
FileMenu = tk.Menu(MenuBar , tearoff=0)
MenuBar.add_cascade(label="文件"  , menu=FileMenu)
FileMenu.add_command(label="新建" , command=NewFile)
FileMenu.add_command(label="打开" , command=ImportFile)
FileMenu.add_command(label="保存" , command=OutportFile)
FileMenu.add_command(label="另存为" , command=ReOutportFile)


FileMenu = tk.Menu(MenuBar , tearoff=0)
MenuBar.add_cascade(label="编辑"  , menu=FileMenu)
FileMenu.add_command(label="新建任务" , command=NewTask)
FileMenu.add_command(label="删除任务" , command=DelTask)
Window.config(menu=MenuBar)

FileMenu = tk.Menu(MenuBar , tearoff=0)
MenuBar.add_cascade(label="帮助"  , menu=FileMenu)
FileMenu.add_command(label="关于 Task Editor" , command=Help)
FileMenu.add_command(label="退出" , command=Exit)
Window.config(menu=MenuBar)
# Blank = tk.Label(Window , font=("" , 5)).pack(side="top")
Info = tk.Label(Window , text="Verson:Dev Anthor:Moxiner").place(x=1640,y=665,anchor="se")


# 配置文件控件样式
ConfigEdit = ttk.Frame(Window)
ConfigEdit_frame = ttk.LabelFrame(ConfigEdit , text="配置文件", padding=(20, 10) )
ConfigEdit_top = ttk.Frame(ConfigEdit_frame)
ConfigEdit_bottom = ttk.Frame(ConfigEdit_frame)
Config_verson_label = ttk.Label(ConfigEdit_top ,text="插件版本")
Config_verson = ttk.Entry(ConfigEdit_top)
Config_verson.bind("<FocusOut>",Save_ConfigEdit)
Config_lang_label = ttk.Label(ConfigEdit_top ,text="插件语言")
Config_lang = ttk.Combobox(ConfigEdit_top , values=["zh_CN","zh_TW","en_US"] ) 
Config_lang.bind("<FocusOut>",Save_ConfigEdit)
Config_money_label = ttk.Label(ConfigEdit_bottom ,text="计分板经济")
Config_money = ttk.Entry(ConfigEdit_bottom) 
Config_money.bind("<FocusOut>",Save_ConfigEdit)
Config_daily_label = ttk.Label(ConfigEdit_bottom ,text="每日任务数量")
Config_daily = ttk.Spinbox(ConfigEdit_bottom , from_=0,to=Any) 
Config_daily.bind("<FocusOut>",Save_ConfigEdit)


ConfigEdit.pack(side="left" ,padx=10)
# 配置文件控件摆放
ConfigEdit_frame.pack(side="top")
ConfigEdit_top.pack(side="top", pady=10)
ConfigEdit_bottom.pack(side="top", pady=10)

Config_verson_label.pack(side="left" ,padx=5)
Config_verson.pack(side="left" , padx=10)
Config_lang_label.pack(side="left" , padx=5)
Config_lang.pack(side="left" , padx=10)
Config_money_label.pack(side="left" ,padx=5)
Config_money.pack(side="left" , padx=10)
Config_daily_label.pack(side="left" , padx=5)
Config_daily.pack(side="left" , padx=10)

# 任务文件控件样式
MainTaskEdit = ttk.LabelFrame(ConfigEdit ,text="任务文件")
MainTaskEdit_left = ttk.Frame(MainTaskEdit)
MainTaskEdit_left_top = ttk.LabelFrame(MainTaskEdit_left , text="子任务" )
MainTaskEdit_left_bottom = ttk.LabelFrame(MainTaskEdit_left , text="主任务")
MainTaskEdit_right = ttk.Frame(MainTaskEdit)

NewTask_button = ttk.Button(MainTaskEdit_left_top , text="新建子任务" , command=NewTask ,width=18)
DelTask_button = ttk.Button(MainTaskEdit_left_top , text="删除子任务" , command=DelTask ,width=18)
MainTask_name = ttk.Entry(MainTaskEdit_left_bottom ,width=18)
SelectMainTask = ttk.Combobox(MainTaskEdit_left_bottom , text="选择任务" , width=18  )
SelectMainTask.bind("<<ComboboxSelected>>", Down_SelecMainTask)
NewMainTask_button = ttk.Button(MainTaskEdit_left_bottom , text="新建任务" , command=DailyTask ,width=18 )
DelMainTask_button = ttk.Button(MainTaskEdit_left_bottom , text="删除任务" , command=DailyTask ,width=18)

Task_Treevive = ttk.Treeview(MainTaskEdit_right , columns=("id" , "name"),show="headings", displaycolumns="#all",height=14)
Task_Treevive.bind("<ButtonRelease-1>", Down_Task_treevive)
Task_Treevive.column("id", width=100 , stretch=True)
Task_Treevive.column("name", width=190 , stretch=True)
Task_Treevive.heading("id", text="子任务ID", anchor="center")
Task_Treevive.heading("name" , text="子任务名", anchor="center" )

# 任务文件控件摆放
MainTaskEdit.pack(side="top" , pady=10)
MainTaskEdit_left.pack(side="left", padx=10, pady=10)
MainTaskEdit_right.pack(side="right" ,padx=10, pady=10)
MainTaskEdit_left_top.pack(side="top" )
MainTaskEdit_left_bottom.pack(side="bottom" , pady=10)
NewTask_button.pack(padx=10, pady=10)
DelTask_button.pack( padx=10, pady=10)
MainTask_name.pack( padx=10, pady=10)
SelectMainTask.pack(padx=10, pady=10)
NewMainTask_button.pack(padx=10, pady=10)
DelMainTask_button.pack(padx=10, pady=10)
Task_Treevive.pack(padx=10, pady=10,expand=1 )



# 任务窗口
TaskWindow = ttk.Frame(Window)
TaskConfig = ttk.Labelframe(TaskWindow , text="基础配置")
TaskConfig_id_label = ttk.Label(TaskConfig , text="任务ID")
TaskConfig_id = ttk.Spinbox(TaskConfig , from_=0 , to= Any ,width=35 ) 
TaskConfig_name_label = ttk.Label(TaskConfig ,text="任务名称")
TaskConfig_name = ttk.Entry(TaskConfig , width=35)
TaskConfig_front_label = ttk.Label(TaskConfig , text="前置任务ID")
TaskConfig_front = ttk.Entry(TaskConfig , width=35)

TaskWindow.pack(side="left")

TaskEdit = ttk.Frame(TaskWindow)
sep1 = ttk.Separator(TaskWindow ,orient="vertical").pack(fill="y" ,expand=True , side="left" ,padx=5)

TaskEdit_conditions = ttk.Labelframe(TaskEdit , text="任务内容")
TaskEdit_conditions_treeview = ttk.Treeview(TaskEdit_conditions , columns=("name" ,"item" , "number" , "mode"),show="headings", displaycolumns="#all")
TaskEdit_conditions_treeview.bind("<ButtonRelease-1>", Down_TaskEdit_conditions_treeview)
TaskEdit_conditions_treeview.column("name", width=100 , stretch=True)
TaskEdit_conditions_treeview.column("item", width=100 , stretch=True)
TaskEdit_conditions_treeview.column("number", width=100 , stretch=True)
TaskEdit_conditions_treeview.column("mode", width=100 , stretch=True)
TaskEdit_conditions_treeview.heading("name", text="名称", anchor="center")
TaskEdit_conditions_treeview.heading("item" , text="物品", anchor="center" )
TaskEdit_conditions_treeview.heading("number" , text="数量", anchor="center" )
TaskEdit_conditions_treeview.heading("mode" , text="模式", anchor="center" )

TaskEdit_conditions_frame1 = ttk.Frame(TaskEdit_conditions)
TaskEdit_conditions_frame2 = ttk.Frame(TaskEdit_conditions)
TaskEdit_conditions_frame3 = ttk.Frame(TaskEdit_conditions)
TaskEdit_conditions_frame4 = ttk.Frame(TaskEdit_conditions)
TaskEdit_conditions_name_label = ttk.Label(TaskEdit_conditions_frame1 , text="内容名称")
TaskEdit_conditions_name = ttk.Entry(TaskEdit_conditions_frame1)
TaskEdit_conditions_object_label = ttk.Label(TaskEdit_conditions_frame1 , text="目标对象")
TaskEdit_conditions_object = ttk.Entry(TaskEdit_conditions_frame1 )
TaskEdit_conditions_aux_label = ttk.Label(TaskEdit_conditions_frame2 , text="特殊值")
TaskEdit_conditions_aux = ttk.Spinbox(TaskEdit_conditions_frame2 ,from_=0 , to=Any , width=50)
# TaskEdit_conditions_ench_label = ttk.Label(TaskEdit_conditions_frame2 , text="附魔属性")
# TaskEdit_conditions_ench = ttk.Entry(TaskEdit_conditions_frame2 )
TaskEdit_conditions_count_label = ttk.Label(TaskEdit_conditions_frame3 ,text="数量")
TaskEdit_conditions_count = ttk.Spinbox(TaskEdit_conditions_frame3 ,from_=0 , to=Any)
TaskEdit_conditions_type_label = ttk.Label(TaskEdit_conditions_frame3 , text="类型")
TaskEdit_conditions_type = ttk.Spinbox(TaskEdit_conditions_frame3 ,values=["item","break","kill"])
TaskEdit_conditions_nametask = ttk.Entry(TaskEdit_conditions_frame4 , text="新建奖励条件")
TaskEdit_conditions_newttask = ttk.Button(TaskEdit_conditions_frame4 , text="新建奖励条件" , width=30)
TaskEdit_conditions_deltask = ttk.Button(TaskEdit_conditions_frame4 , text="删除奖励条件" , width=25)






TaskConfig.pack(side="top" ,padx=10,pady=10)
TaskConfig_id_label.pack(side="left" ,padx=5,pady=10)
TaskConfig_id.pack(side="left" ,padx=5,pady=10)
TaskConfig_name_label.pack(side="left" ,padx=5,pady=10)
TaskConfig_name.pack(side="left" ,padx=10,pady=10)
TaskConfig_front_label.pack(side="left" ,padx=5,pady=10)
TaskConfig_front.pack(side="left" ,padx=10,pady=10)

TaskEdit.pack(side="bottom")
TaskEdit_conditions.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_treeview.pack(side="top")
TaskEdit_conditions_frame1.pack(side="top")
TaskEdit_conditions_frame2.pack(side="top")
TaskEdit_conditions_frame3.pack(side="top")
TaskEdit_conditions_frame4.pack(side="top")
TaskEdit_conditions_name_label.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_name.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_object_label.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_object.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_aux_label.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_aux.pack(side="left" , padx=10,pady=10)
# TaskEdit_conditions_ench_label.pack(side="left" , padx=10,pady=10)
# TaskEdit_conditions_ench.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_count_label.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_count.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_type_label.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_type.pack(side="left" , padx=10,pady=10)
# TaskEdit_conditions_nametask.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_newttask.pack(side="left" , padx=10,pady=10)
TaskEdit_conditions_deltask.pack(side="left" , padx=10,pady=10)



TaskEdit_rewards = ttk.LabelFrame(TaskEdit , text="任务奖励" )
TaskEdit_rewards_treeview = ttk.Treeview(TaskEdit_rewards , columns=("name" ,"item" , "number" , "mode") , show="headings", displaycolumns="#all")
TaskEdit_rewards_treeview.bind("<ButtonRelease-1>", Down_TaskEdit_rewoards_treeview)
TaskEdit_rewards_treeview.column("name", width=100 , stretch=True)
TaskEdit_rewards_treeview.column("item", width=100 , stretch=True)
TaskEdit_rewards_treeview.column("number", width=100 , stretch=True)
TaskEdit_rewards_treeview.column("mode", width=100 , stretch=True)
TaskEdit_rewards_treeview.heading("name", text="名称", anchor="center")
TaskEdit_rewards_treeview.heading("item" , text="物品", anchor="center" )
TaskEdit_rewards_treeview.heading("number" , text="数量" , anchor="center" )
TaskEdit_rewards_treeview.heading("mode" , text="模式", anchor="center" )

TaskEdit_rewards_frame1 = ttk.Frame(TaskEdit_rewards)
TaskEdit_rewards_frame2 = ttk.Frame(TaskEdit_rewards)
TaskEdit_rewards_frame3 = ttk.Frame(TaskEdit_rewards)
TaskEdit_rewards_frame4 = ttk.Frame(TaskEdit_rewards)
TaskEdit_rewards_name_label = ttk.Label(TaskEdit_rewards_frame1 , text="奖励名称")
TaskEdit_rewards_name = ttk.Entry(TaskEdit_rewards_frame1)
TaskEdit_rewards_object_label = ttk.Label(TaskEdit_rewards_frame1 , text="目标对象")
TaskEdit_rewards_object = ttk.Entry(TaskEdit_rewards_frame1 )
TaskEdit_rewards_aux_label = ttk.Label(TaskEdit_rewards_frame2 , text="特殊值")
TaskEdit_rewards_aux = ttk.Spinbox(TaskEdit_rewards_frame2 ,from_=0 , to=Any , width=7)
TaskEdit_rewards_lore_label = ttk.Label(TaskEdit_rewards_frame2 , text="物品命名")
TaskEdit_rewards_lore = ttk.Entry(TaskEdit_rewards_frame2 ,width=10)
TaskEdit_rewards_ench_label = ttk.Label(TaskEdit_rewards_frame2 , text="附魔属性")
TaskEdit_rewards_ench = ttk.Entry(TaskEdit_rewards_frame2 ,width=10)
TaskEdit_rewards_count_label = ttk.Label(TaskEdit_rewards_frame3 ,text="数量")
TaskEdit_rewards_count = ttk.Spinbox(TaskEdit_rewards_frame3 ,from_=0 , to=Any)
TaskEdit_rewards_type_label = ttk.Label(TaskEdit_rewards_frame3 , text="类型")
TaskEdit_rewards_type = ttk.Spinbox(TaskEdit_rewards_frame3 ,values=["item","command","money"])

TaskEdit_rewards_nametask = ttk.Entry(TaskEdit_rewards_frame4 , text="新建奖励条件")
TaskEdit_rewards_newttask = ttk.Button(TaskEdit_rewards_frame4 , text="新建奖励条件" ,width=30)
TaskEdit_rewards_deltask = ttk.Button(TaskEdit_rewards_frame4 , text="删除奖励条件" ,width=30)


TaskEdit_rewards.pack(side="left", padx=10,pady=10)
TaskEdit_rewards_treeview.pack(side="top")
TaskEdit_rewards_frame1.pack(side="top")
TaskEdit_rewards_frame2.pack(side="top")
TaskEdit_rewards_frame3.pack(side="top")
TaskEdit_rewards_frame4.pack(side="top")
TaskEdit_rewards_name_label.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_name.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_object_label.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_object.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_aux_label.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_aux.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_lore_label.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_lore.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_ench_label.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_ench.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_count_label.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_count.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_type_label.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_type.pack(side="left" , padx=10,pady=10)
# TaskEdit_rewards_nametask.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_newttask.pack(side="left" , padx=10,pady=10)
TaskEdit_rewards_deltask.pack(side="left" , padx=10,pady=10)
Help_.place(x=3 ,y=663 ,anchor="sw")
thread()



# 设置主窗口参数
x_cordinate = int((Window.winfo_screenwidth() / 2) - (1650 / 2))
y_cordinate = int((Window.winfo_screenheight() / 2) - (665 / 2))
Window.geometry("1650x665+{}+{}".format(x_cordinate, y_cordinate-20))
Window.tk.call("source", "azure.tcl")
Window.tk.call("set_theme", "light")
Window.mainloop()


# Folderpath = filedialog.askdirectory() #获得选择好的文件夹

