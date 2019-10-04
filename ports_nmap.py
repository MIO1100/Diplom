import socket
from multiprocessing import Pool
import ip as ip_ad
import threading
import nmap

q=0
list=[]
def port_scan(host):

    nm = nmap.PortScanner()
    host = host.strip()
    nm.scan(host)
    result = "Host :" + host + ", (" + nm[host].hostname() + ") " + "State : " + nm[host].state()
    for proto in nm[host].all_protocols():
        lport = nm[host][proto].keys()
        for port in lport:
            list.append(result + "port : " + str(port) + ", state: " + str(nm[host][proto][port]['state']) + ", name: " + str(nm[host][proto][port]['product']))

def start_all():
    main()
    s=list[:]
    return f7(s)

def f7(seq):
    seen = set()
    seen_add = seen.add
    list.clear()
    return [x for x in seq if not (x in seen or seen_add(x))]
def main():
    threads = []
    iprange = ip_ad.get_ip()
    for ip in iprange:
        x = threading.Thread(target=port_scan, args=(ip.strip(),))
        threads.append(x)
        x.start()
    for index, thread in enumerate(threads):
        thread.join()


if __name__ == '__main__':
    result=start_all()
    for i in result:
        print(i)

#https://codeby.net/threads/pishem-hack-tools-mnogopotochnyj-skaner-ip-diapazonov-ehvoljucija.65543/