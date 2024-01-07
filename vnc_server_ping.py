# Detects that a VNC server is running when a host is on
import os

hostname = "" # Hostname or IP address of device running VNC
port = 5900 # Port number of VNC server
api_link = "" # link given by uptime Kuma for PUSH-ing to
filename = str(os.path.abspath(__file__))+"prev_vnc_state"

def rw_file(rw,data):
    file = open(filename,rw)
    if rw == "w":
        file.write(data)
    elif rw == "r":
        return file.read()
    file.close()

def check_vnc_server():
    vnc_status = os.system("nmap -p " + str(port) + " -Pn " + str(hostname) + " | grep 'open'")
    if vnc_status == 0:
        return True
    else:
        return False

response = os.system("ping -c 1 " + hostname)
if response == 0:
    print("[  OK  ] Host",hostname,"is UP")
    if check_vnc_server():
        print("[  OK  ] Host",hostname,"is running a VNC server on port",str(port))
        rw_file("w","1")
        os.system("curl " + api_link)
    else:
        print("[FAILED] Host",hostname,"is not running a VNC server on port",str(port))
        rw_file("w","0")
else:
    print("[FAILED] Host",hostname,"is DOWN")
    if rw_file("r","null") == "1":
        print("[  OK  ] Host",hostname,"was running a VNC server on port",str(port),"before it went down")
        os.system("curl " + api_link)
    else:
        print("[FAILED] Host",hostname,"was not running a VNC server on port",str(port),"before it went down")