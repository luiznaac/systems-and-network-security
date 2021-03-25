import io
from TokenGenerator import TokenGenerator
from datetime import datetime

used_token = {}

class UserToken:

    def __init__(self, parameters):
        self.username = parameters['username']
        self.token = parameters['token']

    def validate(self):
        seed = getSeedPassword(self.username)

        if seed == '':
            return 'not found'

        valid_tokens = TokenGenerator(seed).getActualTokens()

        if self.token in valid_tokens and valid_tokens.index(self.token) < getUsedToken():
            setUsedToken(valid_tokens.index(self.token))
            print(getUsedToken())
            return True

        return False


def getUsedToken():
    now = datetime.now()
    date_time = now.strftime("Y%m%d%%H%M")

    if date_time in used_token.keys():
        return used_token[date_time]

    return 6

def setUsedToken(token_index):
    now = datetime.now()
    date_time = now.strftime("Y%m%d%%H%M")
    used_token[date_time] = token_index


def getSeedPassword(username):
    try:
        file = io.open('seeds/' + username, mode='r', encoding='utf-8')
        seed = file.read()
        file.close()
        return seed
    except:
        return ''
