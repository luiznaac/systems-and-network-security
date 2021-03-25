import io
from TokenGenerator import TokenGenerator
from datetime import datetime

used_tokens = {}

class UserToken:

    def __init__(self, parameters):
        self.username = parameters['username']
        self.token = parameters['token']

    def validate(self):
        seed = getSeedPassword(self.username)

        if seed == '':
            return None

        valid_tokens = TokenGenerator(seed).getActualTokens()
        used_tokens_in_minute = getUsedTokens()

        if self.token in valid_tokens and self.token not in used_tokens_in_minute:
            setUsedToken(self.token)
            print(getUsedTokens())
            return True

        return False


def getUsedTokens():
    now = datetime.now()
    date_time = now.strftime("Y%m%d%%H%M")

    if date_time in used_tokens.keys():
        return used_tokens[date_time]

    return []

def setUsedToken(token):
    now = datetime.now()
    date_time = now.strftime("Y%m%d%%H%M")

    if date_time in used_tokens.keys():
        used_token_in_minute = used_tokens[date_time]
        used_token_in_minute.append(token)
        return

    used_tokens[date_time] = [token]


def getSeedPassword(username):
    try:
        file = io.open('seeds/' + username, mode='r', encoding='utf-8')
        seed = file.read()
        file.close()
        return seed
    except:
        return ''
