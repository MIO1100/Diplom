#!/usr/bin/sudo python


import tkinter as tk
from tkinter import ttk
import psutil
# import iptc
import ports_nmap
import threading
import subprocess
import re
from tkinter.filedialog import *
# from some_table import One_of_some
class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        self.toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        self.btn_open_dialog = tk.Button(self.toolbar, text='Add', command=self.open_dialog, bd=0,
                                    compound=tk.TOP)
        self.btn_save = tk.Button(self.toolbar, text='Save', command=self.save_conf, bd=0,
                                         compound=tk.TOP)
        self.btn_open = tk.Button(self.toolbar, text='Open', command=self.open_conf, bd=0,
                                  compound=tk.TOP)
        # opened ports
        self.txt_system_param = tk.StringVar()
        self.txt_system_param.set("NON")
        self.ports = tk.Scrollbar(self)
        self.list = tk.Listbox(yscrollcommand=self.ports.set, width=100, height=5)
        self.label_system_param = tk.Label(self, textvariable=self.txt_system_param)
        self.iptables_bool = tk.BooleanVar()
        self.check = ttk.Checkbutton(text="firewall status", variable=self.iptables_bool, command= self.off_ok_iptables)
        self.str_table=tk.StringVar()
        self.tables=ttk.Combobox(self, textvariable=self.str_table, state='readonly')
        self.str_chain = tk.StringVar()
        self.chains = ttk.Combobox(self, textvariable=self.str_chain, state='readonly')
        self.btn_delete_rule = ttk.Button(self, text = "Delete rule", command = self.delete_rule)
        self.btn_delete_chain = ttk.Button(self, text = "Delete chain", command = self.delete_chain)
        self.btn_delete_table = ttk.Button(self, text = "Delete table", command = self.delete_table)

        self.scroll_rules = tk.Scrollbar(self)
        self.rules = tk.StringVar(self)
        self.note_with_rules=tk.Listbox(yscrollcommand=self.scroll_rules, listvariable=self.rules, width=100, height=15)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.btn_open_dialog.pack(side=tk.LEFT)
        self.btn_save.pack(side=tk.LEFT)
        self.btn_open.pack(side=tk.LEFT)

        self.list.pack(side=tk.TOP, fill=tk.X)
        self.label_system_param.grid(row=0, column=0, columnspan=4)
        self.check.place(x=0, y=170)
        self.tables.grid(row=1, column=1)
        self.chains.grid(row=1, column=2)
        self.btn_delete_rule.grid(row=2, column=3)
        self.btn_delete_chain.grid(row=2, column=2)
        self.btn_delete_table.grid(row=2, column=1)
        self.note_with_rules.pack(side=tk.BOTTOM)

        self.tables.bind("<<ComboboxSelected>>", lambda event: self.chain_list())
        self.chains.bind("<<ComboboxSelected>>", lambda event: self.list_of_rules())


        x2 = threading.Thread(target=self.check_iptables)
        x2.start()
        x = threading.Thread(target=self.update_ip_ports)
        x.start()
        x1 = threading.Thread(target=self.system_parameters)
        x1.start()

    def delete_chain(self):
        table = self.tables.get()
        chain = self.chains.get()
        subprocess.Popen("sudo nft delete chain "+table+" "+chain, shell=True, stdout=subprocess.PIPE).communicate()
        self.table_list()
    def delete_table(self):
        table = self.tables.get()
        subprocess.Popen("sudo nft delete table " + table, shell=True, stdout=subprocess.PIPE).communicate()
        self.table_list()
    def delete_rule(self):
        select = self.note_with_rules.curselection()[0]
        rule=self.note_with_rules.get(select)
        self.note_with_rules.delete(select)
        handle = re.split(r'handle ', rule)[1]
        table = self.tables.get()
        chain = self.chains.get()
        subprocess.Popen("sudo nft delete rule "+table+" "+chain+" handle "+handle, shell=True, stdout=subprocess.PIPE).communicate()
        self.table_list()
        # about system
    def list_of_rules(self):
        self.note_with_rules.delete(0, tk.END)
        table=self.tables.get()
        chain=self.chains.get()
        chains=self.data.split("table")
        if table in chains[1]:
            rules=chains[1].split("chain")
            rules.pop(0)

        for i in rules:
            if (chain == i[:len(chain)]):
                a = re.sub("^\s+|\r|\t|\s+$", '', i).split("\n")
                break
        for i in a[1:-1]:
            self.note_with_rules.insert(tk.END, i)


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
        self.data = subprocess.Popen("sudo nft --handle list ruleset", shell=True, stdout=subprocess.PIPE).communicate()
        self.data = str(self.data[0], "utf-8")
        self.tables['values']=re.findall(r"table+?(.*)\{", self.data)


        self.chain_list()

    def chain_list(self):
        table=self.tables.get()
        chains=self.data.split("table"+table)
        self.chains["values"]=re.findall(r"chain+?(.*)\{", chains[1])
        # self.chains.current(0)


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
    def save_conf(self):
        f = open(asksaveasfilename(), "w", encoding='utf-8')
        f.write( "#!/usr/sbin/nft -f \n\n flush ruleset \n\n" + subprocess.Popen("sudo nft list ruleset", shell=True, stdout=subprocess.PIPE).communicate()[0].decode("utf-8"))
        f.close()

    def open_conf(self):
        subprocess.call("sudo cp /etc/nftables.conf /etc/nftables_old.conf", shell=True, stdout=subprocess.PIPE)
        subprocess.call("sudo cp "+ askopenfilename() + " /etc/nftables.conf", shell=True, stdout=subprocess.PIPE)


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        self.table = tk.Entry(self)
        self.btn_table = ttk.Button(self, text="Create table", command=self.create_table)
        self.l_table_text = tk.StringVar()
        self.l_table = ttk.Label(self, textvariable=self.l_table_text)


        self.chain = tk.Entry(self)
        self.btn_chain = ttk.Button(self, text="Create chain", command=self.create_chain)
        self.l_chain_text = tk.StringVar()
        self.l_chain = ttk.Label(self, textvariable=self.l_chain_text)


        self.table.grid(row=0, column=0, padx=10, pady=10)
        self.btn_table.grid(row= 0, column=1, padx=10, pady=10)
        self.l_table.grid(row=0, column=2, padx=10, pady=10)

        self.chain.grid(row=2, column=0, padx=10, pady=10)
        self.btn_chain.grid(row=2, column=1, padx=10, pady=10)
        self.l_chain.grid(row=2, column=2, padx=10, pady=10)

    def create_table(self):
        if(self.table.get()!=""):
            if( " " not in self.table.get()):
                subprocess.call("sudo nft add table "+self.table.get(), shell=True, stdout=subprocess.PIPE)
                self.l_table_text.set("Ok")
            else:
                self.l_table_text.set("False")

    def create_chain(self):
        print(1)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("mio")
    root.geometry("900x500")
    root.resizable(False, False)

    root.mainloop()
