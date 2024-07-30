import redis

host = '172.16.147.132'
port = 6379
db = 1
password = 'wns1254'

redisClient = redis.Redis(host=host, port=port, db=db, password=password)