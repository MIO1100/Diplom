import subprocess

subprocess.call("sudo nft add table " + "new ", shell=True, stdout=subprocess.PIPE)
