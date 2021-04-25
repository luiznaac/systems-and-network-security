import io


def persist_txt(path, filename, content):
    file = open(path + '/' + filename + '.txt', 'w+')
    file.write(content)
    file.close()


def load_file(path, filename):
    file = io.open(path + '/' + filename, mode='r', encoding='utf-8')
    content = file.read()
    file.close()
    return content
