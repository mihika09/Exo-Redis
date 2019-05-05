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

v = r.setbit('abc', 9, 1)
print(v)

v = r.setbit('abc', 15, 1)
print(v)

v = r.get('abc')
print("----", v)

v = r.setbit('abc', 6, 1)
print(v)


v = r.get('abc')
print(v)

v = r.setbit('abc', 8, 1)
print(v)

v = r.get('abc')
print(v)
print(v.decode('utf-8'))

v = r.setbit('qwe', 1, 1)
print(v)

v = r.setbit('qwe', 7, 1)
print(v)

v = r.get('qwe')
print(v)

v = r.setbit('qwe', 7, 0)
print(v)

v = r.get('qwe')
print(v)

v = r.setbit('qwe', 7, 0)
print(v)

v = r.get('qwe')
print(v)"""

print(r.zadd('abcd', {"a": 1}))
print(r.zadd('abcd', {"b": 2}))
print(r.zadd('abcd', {"c": 3}))
print(r.zadd('abcd', {"apple": 3}))
print(r.zadd('abcd', {"apple": 2}))
print(r.zcard('abcd'))

"""r.save()
print(v)"""
