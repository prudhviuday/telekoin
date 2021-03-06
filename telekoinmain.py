#import readline


import json
import requests
import time

import redis
import os
import telebot
# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['317172621:AAF_L9Y4vrEK4TUCR7d2TGrjxturuHMk4JA']
#some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
r = redis.from_url(os.environ.get("REDIS_URL"))

#import urllib


#readline.parse_and_bind("tab: complete")

TOKEN = '317172621:AAF_L9Y4vrEK4TUCR7d2TGrjxturuHMk4JA'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)




def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"] #.decode('base64','strict')

        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)




def send_message(text, chat_id):
   # text = text.encode('base64','strict')
    global eth
    text=text+str(eth)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

eth=0
ltc=0

def main():
    global eth,ltc
    print("eth: "+str(eth))
    t=0
    last_update_id = None
    while True:
        t=t+1
	print("eth: "+str(eth))
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)
        if t==30:
            t=0
            #response = urllib2.urlopen('https://koinex.in/api/ticker')
            html = get_url('https://koinex.in/api/ticker')
            data=json.loads(html)
            ltc= data['prices']['LTC']
            eth= data['prices']['ETH']
            print("eth: "+eth)
            
if __name__ == '__main__':
    main()
