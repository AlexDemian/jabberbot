#! /usr/bin/python
#-*- coding: utf8 -*-
import xmpp
import redis
from config import *

class JabClient():

    def __init__(self):
        self.redis = redis.Redis()
        if CLEAN_OLD: self.clean_old()
        self.client = xmpp.Client(DOMAIN, debug=DEBUG, port=PORT)
        self.client.connect()
        self.client.auth(USERNAME, PASSWORD, resource="")
        self.client.RegisterHandler('message', self.message_handler)
        self.client.sendInitPresence()
        self.run_handler()


    def run_handler(self):
        while self.client.Process(0.3):
            get_send = self.redis.lpop(REDIS_SEND_KEY)

            if not get_send:
                continue

            try:
                receiver, message_text = get_send.split("@")
                self.send_mes_to_user(message_text, receiver)
            except:
                print 'Wrong send task:', get_send

    def message_handler(self, connection, message_node):
        try:
            text = str(message_node.getBody())
            user = str(message_node.getFrom())

            if user and text:
                self.redis.lpush(REDIS_RECV_KEY, '%s@%s' % (user.split("@")[0], text))
        except:
            print 'Wrong message(', message_node.getBody(), ') or user(', message_node.getFrom(), ')'

    def send_mes_to_user(self, message_text, receiver):
        message = xmpp.Message('%s@%s' % (receiver, DOMAIN), message_text)
        message.setAttr('type', 'chat')
        self.client.send(message)

    def clean_old(self):
        for key in [REDIS_RECV_KEY, REDIS_SEND_KEY]:
            mess = True
            while mess:
                mess = self.redis.lpop(key)


if __name__ == '__main__':
    JabClient()
