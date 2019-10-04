import os, re

def get_ip():

    f= os.popen("ip a").read()
    result=re.findall(r"[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}(?!255)[0-9]{1,3}",f)
    return result
if __name__ == '__main__':
    print(get_ip())