import uuid
import redis

from app import app


redisHost = app.config['REDIS_HOST']
redisPort = app.config['REDIS_PORT']
redisClient = redis.StrictRedis(redisHost, redisPort)


def gen_random_uuid():
    return uuid.uuid4()


def send_message(channel, message):
    try:
        redisClient.publish(channel, message)
    except Exception as e:
        print(e)
