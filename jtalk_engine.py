import xmpp
import redis



user = "username"
password = "password"

def message_handler(connect_object, message_node):
    redis_rec = redis.Redis()
    try:
        text = str(message_node.getBody())
    except:
        text = "help"
    user = str(message_node.getFrom())
    if user and text:
        redis_rec.lpush("jabrec", user.split("@")[0]+"@"+text)


def send_mes_to_user(message_text, receivers):
    for rec in receivers:
        message = xmpp.Message(rec+'@domain.com', message_text)
        message.setAttr('type', 'chat')
        client.send(message)


jid = xmpp.JID(user)
client = xmpp.Client('domain.com', debug=False, port=5223)
client.connect()
client.auth(user, password, resource="")

client.RegisterHandler('message', message_handler)
client.sendInitPresence()

redis_send = redis.Redis()
while client.Process(0.3):
    get_send = redis_send.lpop("jabsend")
    if get_send:
        try:
            receivers, message_text = get_send.split("@")
            send_mes_to_user(message_text, receivers.split(","))
        except:
            pass








