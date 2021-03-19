import hashlib

class User:

    def __init__(self, parameters):
        self.username = parameters['username']
        self.seed_password = self.generateHash(parameters['seed_password'])
        self.password = self.generateHash(parameters['password'])

    def generateHash(self, entry):
        generator = hashlib.sha256()
        generator.update(str.encode(entry))
        return generator.hexdigest()

    def persist(self):
        file = open('users/' + self.username, 'w+')
        file.write('seed:' + self.seed_password + '\n')
        file.write('pass:' + self.password)
        file.close()
