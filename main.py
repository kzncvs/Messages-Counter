import vk_api

targetID = 70439813  # ID of target dialog. +2000000000 for group chat ID
login, password = '', ''  # Your VK login and password
vk_session = vk_api.VkApi(login, password)
try:
    vk_session.authorization()
except vk_api.AuthorizationError as error_msg:
    print(error_msg)
vk = vk_session.get_api()

vault = []
off = 0

while True:
    kek = vk.messages.getHistory(peer_id=targetID, offset=off, count=200)
    off += 200
    vault.extend(kek['items'])
    if len(kek['items']) < 200:
        break

byUsers = {}

for i in range(len(vault)):
    try:
        byUsers[str(vault[i]['from_id'])] += 1
    except KeyError:
        byUsers[str(vault[i]['from_id'])] = 1

ids = []
cou = []
for i in byUsers:
    ids.append(i)
    cou.append(byUsers[i])

n = 1
while n < len(cou):
    for i in range(len(cou) - n):
        if cou[i] > cou[i + 1]:
            cou[i], cou[i+1] = cou[i+1], cou[i]
            ids[i], ids[i+1] = ids[i+1], ids[i]
    n += 1

finalMessage = ''
for i in range(len(ids)):
    userName = vk.users.get(user_ids=ids[i])
    finalMessage = (finalMessage + userName[0]['first_name'] + ' '
                    + userName[0]['last_name'] + ' ' + str(cou[i]) + '\n')

vk.messages.send(peer_id=targetID, message=str(finalMessage))
