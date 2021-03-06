import requests

url = "http://127.0.0.1:1337"
auth = ("username_here", "password_here")

a = requests.get(url)
print(a.content.decode('utf8'))
print(a.status_code)

url += "/api"

a = requests.post(url + "/users", json={"username": auth[0], "password": auth[1]})
print(a.content.decode('utf8'))
print(a.status_code)

print("-------------------------------------------------------------")
print("GET ALL FEEDS")
b = requests.get(url + "/feeds", auth=auth)
print(b.text)
print(b.status_code)

print("-------------------------------------------------------------")
print("FOLLOW FEED 2")
c = requests.post(url + "/feeds/follow", auth=auth, json={'feed_id': '2'})
print(c.text)
print(c.status_code)

print("-------------------------------------------------------------")
print("FOLLOW FEED 1")
c = requests.post(url + "/feeds/follow", auth=auth, json={'feed_id': '1'})
print(c.text)
print(c.status_code)

print("-------------------------------------------------------------")
print("GET MY FEEDS")
d = requests.get(url + "/my-feeds", auth=auth)
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("GET UNREAD ITEMS FROM FEED 2")
d = requests.get(url + "/my-feeds/2/new", auth=auth)
print(d.text)
print(d.status_code)


print("-------------------------------------------------------------")
print("GET UNREAD FROM ALL FEEDS THAT I FOLLOW")
d = requests.get(url + "/my-feeds/new", auth=auth)
print(d.text)
print(d.status_code)


print("-------------------------------------------------------------")
print("READ FEED ITEM 49")
x = requests.post(url + "/items/49/read", auth=auth)
print(x.text)
print(x.status_code)

print("-------------------------------------------------------------")
print("READ MULTIPLE FEED ITEMS")
x = requests.post(url + "/items/read-multiple", auth=auth, json={'item_ids': [1,  2,  3,  4,  5,  6,  7,  8,  9, 10]})
print(x.text)
print(x.status_code)

print("-------------------------------------------------------------")
print("GET READ ITEMS FROM FEED 2")
d = requests.get(url + "/my-feeds/2/old", auth=auth)
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("GET READ FROM ALL FEEDS THAT I FOLLOW")
d = requests.get(url + "/my-feeds/old", auth=auth)
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("GET UNREAD FROM ALL FEEDS THAT I FOLLOW")
d = requests.get(url + "/my-feeds/new", auth=auth)
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("REFRESH SINGLE FEED")
d = requests.post(url + "/my-feeds/1/update", auth=auth)
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("UNFOLLOW FEED 2")
c = requests.delete(url + "/feeds/unfollow", auth=auth, json={'feed_id': '2'})
print(c.text)
print(c.status_code)

print("-------------------------------------------------------------")
print("UNFOLLOW FEED 1")
c = requests.delete(url + "/feeds/unfollow", auth=auth, json={'feed_id': '1'})
print(c.text)
print(c.status_code)

print("-------------------------------------------------------------")
print("GET MY FEEDS")
d = requests.get(url + "/my-feeds", auth=auth)
print(d.text)
print(d.status_code)

print("-------------------------------------------------------------")
print("READ FEED ITEM 49")
x = requests.post(url + "/items/49/read", auth=auth)
print(x.text)
print(x.status_code)

