import redis
import time
import json
import sendgrid

import config

from app.controllers import activate


redisClient = redis.StrictRedis(config.REDIS_HOST, config.REDIS_PORT)

receiver = redisClient.pubsub()
receiver.subscribe(activate.channel)


while True:
    message = receiver.get_message()

    if(message):
        type_message = message["type"]

        if(type_message == "message"):
            try:
                channel = message["channel"].decode("utf-8")
                data = message["data"].decode("utf-8")
                content = json.loads(data)

                if channel == activate.channel:
                    activate.handle_message(content)

            except Exception as e:
                print(e)
                print(message)

    time.sleep(0.001)

