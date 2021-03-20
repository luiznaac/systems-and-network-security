import random
from datetime import datetime

class TokenGenerator:

    def __init__(self, seed):
        self.seed = seed

    def getActualTokens(self):
        now = datetime.now()
        date_time = now.strftime("Y%m%d%%H%M")
        random.seed(self.seed + date_time)

        tokens = []
        for i in range(0, 6):
            generated_token = str(int.from_bytes(random.randbytes(8), 'big'))
            tokens.append(generated_token[0:6].zfill(6))

        return tokens
