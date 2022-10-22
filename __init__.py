import json

class Cfg:
    file = open('data/config/cfg.json', 'r')
    content = json.loads(file.read())
    file.close()
    token = content['token']
    adminId = content['adminId']
    commision = content['commision']
    sleepChecking = content['sleepChecking']
    adminQiwi = content['adminQiwi']

    def save(self, adminQiwi, commision):
        file = open('data/config/cfg.json', 'r')
        content = json.loads(file.read())
        file.close()
        content['adminQiwi'] = adminQiwi
        content['commision'] = commision
        file = open('data/config/cfg.json', 'w')
        json.dump(content, file)
        file.close()

