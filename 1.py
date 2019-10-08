#!/usr/bin/sudo python


import tkinter as tk
from tkinter import ttk
import psutil
# import iptc
import ports_nmap
import threading
import subprocess
import re
# from some_table import One_of_some
class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        # self.my_threads=[]

        self.toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        self.btn_open_dialog = tk.Button(self.toolbar, text='Add', command=self.open_dialog, bd=0,
                                    compound=tk.TOP)
        # opened ports
        self.txt_system_param = tk.StringVar()
        self.txt_system_param.set("NON")
        self.ports = tk.Scrollbar(self)
        self.list = tk.Listbox(yscrollcommand=self.ports.set, width=100, height=5)

        self.label_system_param = tk.Label(self, textvariable=self.txt_system_param)

        self.iptables_bool = tk.BooleanVar()
        self.check = ttk.Checkbutton(text= "firewall status", variable=self.iptables_bool, command= self.off_ok_iptables)


        self.str_table=tk.StringVar()
        self.tables=ttk.Combobox(self, textvariable=self.str_table)


        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.btn_open_dialog.pack(side=tk.LEFT)
        self.list.pack(side=tk.TOP, fill=tk.X)
        self.label_system_param.grid(row=0, column=0, columnspan=4)
        self.check.place(x=0, y=170)
        self.tables.grid(row=1, column=1)

        x2 = threading.Thread(target=self.check_iptables)
        x2.start()
        x = threading.Thread(target=self.update_ip_ports)
        x.start()
        x1 = threading.Thread(target=self.system_parameters)
        x1.start()

        # about system

    def system_parameters(self):
        mem = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=2, percpu=True)
        s = 'Power on '
        j = 0
        for i in cpu:
            s = s + str(j) + ' core: ' + str(i) + '%, '
            j += 1
        s = s + '. \nRAM occupied: ' + str(mem) + '%'
        self.txt_system_param.set(s)
        # print(s)
        self.after(100000, self.system_parameters)

    def table_list(self):
        data = subprocess.Popen("sudo nft list ruleset", shell=True, stdout=subprocess.PIPE).communicate()
        data = str(data[0], "utf-8")
        self.tables['values']=re.findall(r"table+?(.*)\{", data)



    def check_iptables(self):
        data = subprocess.Popen("sudo systemctl status nftables", shell=True, stdout=subprocess.PIPE).communicate()
        self.table_list()
        if (bytearray(b' active') in data[0]):
            self.iptables_bool.set(True)
        elif (bytearray(b'inactive') in data[0]):
            self.iptables_bool.set(False)
        else:
            print("error check")

    def off_ok_iptables(self):
        if (self.iptables_bool.get() == False):
            self.iptables_bool.set(False)
            subprocess.call("sudo systemctl stop nftables", shell=True, stdout=subprocess.PIPE)
        else:
            self.iptables_bool.set(True)
            print(self.iptables_bool.get())
            subprocess.call("sudo systemctl start nftables", shell=True, stdout=subprocess.PIPE)
        self.table_list()


    def update_ip_ports(self):
        ip_ports = ports_nmap.start_all()
        for ip_port in ip_ports:
            self.list.insert(tk.END, ip_port)
        self.ports.config(command=self.list.yview)
        self.after(100000, self.update_ip_ports)


    def open_dialog(self):
        Child()
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        print("11111111111")


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("mio")
    root.geometry("900x500")
    root.resizable(False, False)

    root.mainloop()
