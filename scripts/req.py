import requests
from passlib.context import CryptContext

url = "http://127.0.0.1:5000/api"

# a = requests.get(url)
# print(a.content.decode('utf8'))
# print(a.status_code)
#
#
# a = requests.post(url + "/users", json={"username": "svet", "password": "123"})
# print(a.content.decode('utf8'))
# print(a.status_code)

print("-------------------------------------------------------------")
print("GET ALL FEEDS")
b = requests.get(url + "/feeds", auth=('svet', '123'))
print(b.text)
print(b.status_code)

print("-------------------------------------------------------------")
print("FOLLOW FEED 2")
c = requests.post(url + "/feeds/follow", auth=('svet', '123'), json={'feed_id': '2'})
print(c.text)
print(c.status_code)

print("-------------------------------------------------------------")
print("FOLLOW FEED 1")
c = requests.post(url + "/feeds/follow", auth=('svet', '123'), json={'feed_id': '1'})
print(c.text)
print(c.status_code)

print("-------------------------------------------------------------")
print("GET MY FEEDS")
d = requests.get(url + "/my-feeds", auth=('svet', '123'))
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("GET UNREAD ITEMS FROM FEED 2")
d = requests.get(url + "/my-feeds/2/new", auth=('svet', '123'))
print(d.text)
print(d.status_code)


print("-------------------------------------------------------------")
print("GET UNREAD FROM ALL FEEDS THAT I FOLLOW")
d = requests.get(url + "/my-feeds/new", auth=('svet', '123'))
print(d.text)
print(d.status_code)


print("-------------------------------------------------------------")
print("READ FEED ITEM 49")
x = requests.post(url + "/items/49/read", auth=('svet', '123'))
print(x.text)
print(x.status_code)

print("-------------------------------------------------------------")
print("READ MULTIPLE FEED ITEMS")
x = requests.post(url + "/items/read-multiple", auth=('svet', '123'), json={'item_ids': [1,  2,  3,  4,  5,  6,  7,  8,  9, 10]})
print(x.text)
print(x.status_code)

print("-------------------------------------------------------------")
print("GET READ ITEMS FROM FEED 2")
d = requests.get(url + "/my-feeds/2/old", auth=('svet', '123'))
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("GET READ FROM ALL FEEDS THAT I FOLLOW")
d = requests.get(url + "/my-feeds/old", auth=('svet', '123'))
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("GET UNREAD FROM ALL FEEDS THAT I FOLLOW")
d = requests.get(url + "/my-feeds/new", auth=('svet', '123'))
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("REFRESH SINGLE FEED")
d = requests.post(url + "/my-feeds/1/update", auth=('svet', '123'))
print(d.text)
print(d.status_code)


print("-------------------------------------------------------------")
print("UNFOLLOW FEED 2")
c = requests.delete(url + "/feeds/unfollow", auth=('svet', '123'), json={'feed_id': '2'})
print(c.text)
print(c.status_code)

print("-------------------------------------------------------------")
print("UNFOLLOW FEED 1")
c = requests.delete(url + "/feeds/unfollow", auth=('svet', '123'), json={'feed_id': '1'})
print(c.text)
print(c.status_code)

# print("-------------------------------------------------------------")
# print("GET MY FEEDS")
# d = requests.get(url + "/my-feeds", auth=('svet', '123'))
# print(d.text)
# print(d.status_code)
#
# print("-------------------------------------------------------------")
# print("READ FEED ITEM 49")
# x = requests.post(url + "/items/49/read", auth=('svet', '123'))
# print(x.text)
# print(x.status_code)
#
