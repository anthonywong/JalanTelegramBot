#!/usr/bin/env python3

# Copyright (c) 2016 Anthony Wong <yp@anthonywong.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

import sys
import time
import random
import datetime
import telepot
import urllib3
from pprint import pprint

links = {}
search_str = '申し訳ありませんが、設定された条件でご利用できるプランがないか、宿がじゃらんnetでの予約受付を停止中です。'

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    #print( 'Got command: %s' % command)
    pprint(msg)

    if command.startswith('/add '):
        url = command[5:]
        if url.startswith('http://') or url.startswith('https://'):
            if chat_id not in links:
                links[chat_id] = [ url ]
            else:
                links[chat_id].append(url)
            bot.sendMessage(chat_id, 'URL ' + url + ' added')
        else:
            bot.sendMessage(chat_id, 'Wrong URL format: ' + url)
        pprint(links)
    elif command.startswith('/del ') or command.startswith('/remove '):
        url = command[command.find(' ')+1:]
        try:
            links[chat_id].remove(url)
        except ValueError as e:
            pass

def checkWeb():
    for chat_id, v in links.items():
        for link in v:
            print('Checking ' + link + '...')
            pool = urllib3.PoolManager()
            header = urllib3.make_headers(user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.6 Safari/537.36')
            r = pool.request('GET', link, headers=header)
            html = r.data.decode('shift-jis').encode('utf-8').decode('utf-8')
            #pprint(html)
            if search_str not in html:
                bot.sendMessage(chat_id, 'ALERT! Room available: ' + link)
            #pprint(r.data)

bot = telepot.Bot('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
bot.notifyOnMessage(handle)
print('I am listening ...')

while 1:
    time.sleep(300)
    if len(links) > 0:
        checkWeb()
