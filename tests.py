import redis

r = redis.Redis(
	host="127.0.0.1",
	port=15000
)

"""r.set('foo', 'bar')

v = r.get('foo')
print(v)

v = r.getbit('foo', 0)
print(v)

v = r.getbit('foo', 3)
print(v)

v = r.getbit('foo', 6)
print(v)

v = r.getbit('foo', 50)
print(v)"""

"""r.set('abc', 'A')

v = r.get('abc')
print(v)

v = r.setbit('abc', 6, 1)
print(v)

v = r.get('abc')
print(v)

v = r.setbit('abc', 8, 1)
print(v)

v = r.get('abc')
print(v)
# print(v.decode('utf-8'))

v = r.setbit('qwe', 1, 1)
print(v)

v = r.setbit('qwe', 7, 1)
print(v)

v = r.get('qwe')
print(v)"""


r.zadd('abc', {"a": 1})
r.zadd('abc', {"b": 2})
r.zadd('abc', {"c": 3})
r.zadd('abc', {"apple": 3})
r.zadd('abc', {"apple": 2})

"""r.save()
print(v)"""
