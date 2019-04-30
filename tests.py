import redis

r = redis.Redis(
	host="127.0.0.1",
	port=15000
)

print("ABC")
r.set('foo', 'bar')
print("Hello")
v = r.get('foo')