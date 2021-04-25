import io
import hashlib
import des
import base64


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
    encrypted_data = des_key.encrypt(bytes(data, 'utf8'), initial=None, padding=True)
    return str(base64.b64encode(encrypted_data), 'utf8')


def des_decrypt(data, key):
    des_key = des.DesKey(bytes(key, 'utf8'))
    encrypted_data = base64.b64decode(data)
    decrypted_data = des_key.decrypt(encrypted_data, initial=None, padding=True)
    return str(decrypted_data, 'utf8')
