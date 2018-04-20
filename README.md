Simple python xmpp bot.
Redis used as fast buffer

Requairements:
1) python 2.7

2) Redis
https://redis.io/

3) Python/xmpp library

Usage:
After installation of all libreries specify your xmpp-account settings at config.py

Then run xmppbot.py in loop:
> python xmppbot.py

And try to send and receive messages via commandline:

To receive message:

> redis-cli lpop recv_mess

To send message:

> redis-cli lpush send_mess username@message