import tkinter as tk
import paramiko
from tkinter import ttk
import re

'''def Get_filling_information():
    global ip_addr
    global sw_port
    global get_username
    global get_password
    ip_addr = ip_entry.get()
    sw_port = port_entry.get()
    get_username = username_entry.get()
    get_password = password_entry.get()
    if ip_addr == "":
        print("请输入正确的IP地址")
    if sw_port == "":
        print("请填写端口号")""
'''
ssh_client = None
selected_encoding = 'utf-8'


# 创建主窗口
window = tk.Tk()
window.title("网络交换机调试工具")
window.geometry("840x400")
window.resizable(False, False)

# 第一行提示
protocol_label = tk.Label(window, text="选择连接的协议")
protocol_label.grid(row=0, column=0,columnspan=2,pady=1)

# 第二行，三个单选按钮
protocol_var = tk.StringVar()
protocol_var.set("SSH")

ssh_radio = tk.Radiobutton(window, text="SSH", variable=protocol_var, value="SSH")
telnet_radio = tk.Radiobutton(window, text="Telnet", variable=protocol_var, value="Telnet")
com_radio = tk.Radiobutton(window, text="Com口", variable=protocol_var, value="Com口")
ssh_radio.grid(row=1, column=0,stick="W")
telnet_radio.grid(row=1, column=1,stick="W")
com_radio.grid(row=1, column=2,stick="W")

# 第三行，IP地址输入
ip_label = tk.Label(window, text="IP地址：")
ip_label.grid(row=2, column=0,stick="W")
ip_entry = tk.Entry(window)
ip_entry.grid(row=2, column=1,columnspan=2,stick="W")

# 第三行，用户名输入
username_label = tk.Label(window, text="用户名：")
username_label.grid(row=3, column=0,stick="W")
username_entry = tk.Entry(window)
username_entry.grid(row=3, column=1,columnspan=2,stick="W")

# 第四行，密码输入
password_label = tk.Label(window, text="密码：")
password_label.grid(row=4, column=0,stick="W")
password_entry = tk.Entry(window,show="*")
password_entry.grid(row=4, column=1,columnspan=2,stick="W")

# 第五行，端口输入
port_label = tk.Label(window, text="端口：")
port_label.grid(row=5, column=0,stick="W")
port_entry = tk.Entry(window)
port_entry.insert(0,22)
port_entry.grid(row=5, column=1,columnspan=2,stick="W")

def handle_selection(event=None):
    global selected_encoding
    selected_encoding = combo.get()
    print(f"选择的编码是：{selected_encoding}")
    debug_text.insert(tk.END,f"选择的编码是：{selected_encoding}\n")
    debug_text.see(tk.END)

#定义一个编码的选择复选框
combo = ttk.Combobox(window, values=["gbk", "utf-8"], width=5)
combo.set("utf-8")
combo.grid(row=6, column=2)
combo.bind("<<ComboboxSelected>>", handle_selection)

# 第六行，连接和断开按钮
def connect():
    global selected_encoding
    protocol = protocol_var.get()
    username = username_entry.get()
    password = password_entry.get()
    hostname = ip_entry.get()
    port = port_entry.get()
    print(f"protocol={protocol},username={username},password={password},hostname={hostname},port={port}")

    #判断用户是否输入了连接主机的信息
    variables = {"username": username, "password": password, "hostname": hostname, "port": port}
    for key, value in variables.items():
        if not value:
            print(f"{key} 为空，请输入")
            debug_text.insert(tk.END, f"{key}为空，请输入\n")
            debug_text.see(tk.END)

    if protocol == "SSH":
        # SSH连接处理
        global ssh_client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 设置SSH连接选项，如端口、用户名、密码等
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)

        # 发送命令并接收返回结果
        #stdin, stdout, stderr = ssh_client.exec_command('show confi')
        #output = stdout.read().decode(selected_encoding)
        #error = stderr.read().decode(selected_encoding)
        #print(f"Output: {output}")
        #print(f"Error: {error}")
        #debug_text.insert(tk.END, f"Output: {output}\n")
        #debug_text.insert(tk.END, f"Error: {error}\n")
        debug_text.insert(tk.END, f"已连接至{hostname}服务器\n")
        debug_text.see(tk.END)
        print('已连接')

    #if protocol == "Telnet":
    # Telnet连接处理


    #elif protocol == "Com口":
# Com口连接处理
# ...

def disconnect():
    # 断开连接处理
    # ...
    global ssh_client

    if ssh_client is None:
        print('未连接任何服务器')
        debug_text.insert(tk.END, "未连接任何服务器\n")
        debug_text.see(tk.END)
    else:
        ssh_client.close()
        ssh_client = None
        print(f'断开链接')
        debug_text.insert(tk.END, f"断开连接\n")
        debug_text.see(tk.END)

def send_command():
    command = command_entry.get()
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode()
    command_entry.delete(0,tk.END)
    debug_text.insert(tk.END,command + "\n")
    debug_text.see(tk.END)
    update_debug_text(output)

def update_debug_text(message):
    debug_text.configure(state='normal')
    debug_text.insert(tk.END, message + "\n")
    debug_text.see(tk.END)
    debug_text.configure(state='disabled')

connect_button = tk.Button(window, text="连接",command=connect,fg="red",bg="green")
connect_button.grid(row=6, column=0)
disconnect_button = tk.Button(window, text="断开",command=disconnect)
disconnect_button.grid(row=6, column=1)


# 第七行提示
port_config_label = tk.Label(window, text="H3c 交换机端口配置",)
port_config_label.grid(row=7, column=0,columnspan=2,pady=(0,0))

# 第八行，选项复选框和接口输入框
port_type_var = tk.StringVar()
port_type_var.set("access")

trunk_checkbox = tk.Checkbutton(window, text="Trunk口", variable=port_type_var, onvalue="trunk")
access_checkbox = tk.Checkbutton(window, text="Access口", variable=port_type_var, onvalue="access")
trunk_checkbox.grid(row=8, column=0,stick="W")
access_checkbox.grid(row=8, column=1,stick="W")
#trunk_checkbox.pack(side="left")
#access_checkbox.pack(side="left")

port_config_entry = tk.Entry(window)
port_config_entry.grid(row=9, column=0,stick="W",columnspan=2)



#
test_label = tk.Label(window, text="调试窗口")
test_label.grid(row=0, column=3,stick="W")


# 右侧调试窗口
debug_text = tk.Text(window,borderwidth=3)
debug_text.grid(row=1, column=3, rowspan=8,padx=5,pady=5)

# 创建垂直滑动条
scrollbar = tk.Scrollbar(window)
scrollbar.grid(row=1, column=4, rowspan=8, sticky='ns',padx=5, pady=5)

debug_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=debug_text.yview)

def CommandSub():
    Command_input_window=command_entry.get()
    debug_text.insert(tk.END,Command_input_window+ "\n")
    command_entry.delete(0,tk.END)

#命令交互输入窗口
command_entry = tk.Entry(window,borderwidth=3,width=80)
command_entry.grid(row=9,column=3,stick="W",padx=5)
command_entry.bind("<Return>", lambda event: send_command())

#命令提交按钮。
command_submit = tk.Button(window, text="提交",command=send_command)
command_submit.grid(row=9,column=4,stick="W")


window.mainloop()
