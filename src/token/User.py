import hashlib
import io

class User:

    def __init__(self, parameters):
        self.username = parameters['username']
        self.seed_password = parameters['seed_password']
        self.password = parameters['password']

    def persist(self):
        file = open('users/' + self.username, 'w+')
        file.write(generateHash(self.password))
        file.close()
        file = open('seeds/' + self.username, 'w+')
        file.write(generateHash(self.seed_password))
        file.close()



def generateHash(entry):
    generator = hashlib.sha256()
    generator.update(str.encode(entry))
    return generator.hexdigest()


def loadUser(parameters):
    info = getFileInfo(parameters['username'])

    if info == '':
        return None

    user_info = {
        'username': parameters['username'],
        'seed_password': info[0],
        'password': info[1],
    }

    if user_info['password'] != generateHash(parameters['password']):
        return 'wrong password'

    return User(user_info)


def getFileInfo(username):
    try:
        file = io.open('users/' + username, mode='r', encoding='utf-8')
        password = file.read()
        file.close()
        file = io.open('seeds/' + username, mode='r', encoding='utf-8')
        seed = file.read()
        file.close()
        return [seed, password]
    except:
        return ''
