import redis

r = redis.Redis(
	host="127.0.0.1",
	port=15000
)

r.set('foo', 1)

v = r.set('bar', '1')

"""v = r.get('foo')
print(v)

r.save()
print(v)"""
