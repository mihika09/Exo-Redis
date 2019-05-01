import redis

r = redis.Redis(
	host="127.0.0.1",
	port=15000
)

r.set('foo', 'bar')

v = r.get('foo')
print(v)

v = r.getbit('foo', 0)
print(v)

v = r.getbit('foo', 3)
print(v)

v = r.getbit('foo', 6)
print(v)

v = r.getbit('foo', 50)
print(v)

"""r.save()
print(v)"""
