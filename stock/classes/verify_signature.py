from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def verify_signature():
    with open("Подпись.txt", 'rb') as f:
        sign = f.read()
    f.close()

    with open("Ключ.pem", 'rb') as f:
        key_data = f.read()
        pubkey = RSA.import_key(key_data)

    # Получаете хэш файла
    file_hash = SHA256.new()
    with open("Отчет.docx", "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            file_hash.update(chunk)
    # Отличающийся хэш не должен проходить проверку
    try:
        pkcs1_15.new(pubkey).verify(file_hash, sign)
        return "Проверка пройдена успешно"
    except ValueError:
        return "Файл не прошел проверку"
