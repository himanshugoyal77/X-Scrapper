import threading
import queue

import requests

q = queue.Queue()

valid_proxies = []

with open('proxies.txt') as f:
    proxies = f.read().split('\n')
    for p in proxies:
        q.put(p)
        
def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            r = requests.get('http://ipinfo.io/json', 
                             proxies={'http': proxy, 
                                      'https': proxy}, 
                             timeout=5)
            if r.status_code == 200:
                valid_proxies.append(proxy)
                #write in a file
                with open('valid_proxies.txt', 'a') as f:
                    f.write(proxy + '\n')
        except:
            continue
        

for _ in range(10):
    t = threading.Thread(target=check_proxy)
    t.start()



