class User:

    def __init__(self, parameters):
        self.username = parameters['username']
        self.seed_password = parameters['seed_password']
        self.password = parameters['password']
