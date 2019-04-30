import redis

r = redis.Redis(
	host="127.0.0.1",
	port=15000
)

v = r.set('foo', 'bar')
print(v)

v = r.get('foo')
print(v)

r.save()
print(v)
