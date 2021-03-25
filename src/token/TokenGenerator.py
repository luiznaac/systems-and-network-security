from datetime import datetime
import hashlib

class TokenGenerator:

    def __init__(self, seed):
        self.seed = seed

    def getActualTokens(self):
        now = datetime.now()
        date_time = now.strftime("Y%m%d%%H%M")
        generator = hashlib.sha256()
        generator.update(bytes(self.seed + date_time, 'utf-8'))

        tokens = []
        for i in range(0, 6):
            generated_token = generator.digest()
            tokens.append(str(int.from_bytes(generated_token[0:4], 'big'))[0:6])
            generator.update(generated_token)

        return tokens
