import io
import hashlib
import des


def persist_txt(path, filename, content):
    file = open(path + '/' + filename + '.txt', 'w+')
    file.write(content)
    file.close()


def load_file(path, filename):
    file = io.open(path + '/' + filename, mode='r', encoding='utf-8')
    content = file.read()
    file.close()
    return content


def generate_hash(entry):
    generator = hashlib.sha256()
    generator.update(str.encode(entry))
    return generator.hexdigest()[0:24:]


def des_encrypt(data, key):
    des_key = des.DesKey(bytes(key, 'utf8'))
    return des_key.encrypt(bytes(data, 'utf8'), initial=None, padding=True)


def des_decrypt(data, key):
    des_key = des.DesKey(bytes(key, 'utf8'))
    return des_key.decrypt(data, initial=None, padding=True)
