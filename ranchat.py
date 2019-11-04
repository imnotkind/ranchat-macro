from websocket import create_connection
import threading
import time
import requests
import re
from confusable_homoglyphs import confusables

def namuchat(i):
    options = {}
    options["subprotocols"] = ["chat"]

    ws = create_connection("wss://chat.namu.live/chat", **options)
    print(str(i), "open")

    r = ws.recv()
    assert r=="accept"

    ws.send("붸에에에엙")
    ws.close()
    print(str(i), "close")

def gagachat(i):
    t = round(time.time()*1000)
    r = requests.get("http://www.gagalive.com/randomchat/js/?c="+str(t)).text
    #print(r)

    key = ["Y"+r[r.index("4e4|")+4:r.index("|24e4")], "L손님_" + r[r.index("ub2d8_")+6:r.index("|uc624")] + "|@@@randomchat" ]
    print(key)

    ws = create_connection("ws://rchat.gagalive.kr:8080/")
    print(str(i), "open")

    ws.send(key[0])
    ws.send(key[1])

    time.sleep(0.5)

    time.sleep(0.1)
    ws.send("#!)*")

    time.sleep(0.1)
    ws.send("#붸에에에에ㅔㄱ")

    while True:
        r = ws.recv()
        print("RECV",r)
        spam = "스팸 방지 문자: "
        if r.find(spam) != -1:
            s = r[r.find(spam) + len(spam):]
            print("CAPTCHA", s)
            ss = ""
            for c in s:
                a = confusables.is_confusable(c, greedy=True)
                print(a)
                if a == False:
                    ss += c
                    continue
                for p in a:
                    found = False
                    for q in p['homoglyphs']:
                        if q['n'].find("DIGIT") == 0 or q['n'].find(", DIGIT") != -1:
                            ss += q['c']
                            found = True
                            break
                    if not found:
                        ss += c
            ss = ss.replace(" ","").replace(")","").replace("(","")
            print("CAPTCHA DECODE", ss)
            ws.send("#" + ss)


    print(str(i), "shut down")





batch = 1

while True:
    l = []
    for i in range(batch):
        t = threading.Thread(target=namuchat, args=(i,))
        t.daemon = True
        l.append(t)
    for i in range(batch):
        l[i].start()
    for i in range(batch):
        l[i].join()

    print("batch complete")

