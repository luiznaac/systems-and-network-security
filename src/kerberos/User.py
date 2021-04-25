import utils


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def persist(self):
        utils.persist_txt('users', self.username, self.password)


def load_user(parameters):
    user_info = {
        'username': parameters['username'],
        'password': utils.load_file('users', parameters['username'])[0],
    }

    return User(user_info)
