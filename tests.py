import redis

r = redis.Redis(
	host="127.0.0.1",
	port=15000
)

print("\n***SET and GET***\n")

print(r.set('foo', 'bar'))

v = r.get('foo')
print(v)


r.set('abc', '1010')
r.set('def', 'amazing')

v = r.get('abc')
print(v)

v = r.get('def')
print(v)

print("\n***SETBIT and GETBIT***\n")

print("setbit: ", r.setbit("test", 1, 1))
print("setbit: ", r.setbit("test", 7, 1))
print("getbit: ", r.getbit("test", 7))
print("get: ", r.get("test"))
print("setbit: ", r.setbit("test", 7, 0))
print("getbit: ", r.getbit("test", 7))
print("get: ", r.get("test"))
print("setbit: ", r.setbit("test", 8, 1))
print("get: ", r.get("test"))

print("\n***Z - COMMANDS***\n")

print(r.zadd('abcd', {"a": 1}))
print(r.zadd('abcd', {"b": 2}))
print(r.zadd('abcd', {"c": 3}))
print(r.zadd('abcd', {"apple": 3}))
print(r.zadd('abcd', {"apple": 2}))
print(r.zcard('abcd'))
print(r.zcount('abcd', 1, 3))

"""r.save()
print(v)"""
