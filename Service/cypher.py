import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Cypher:
    __password = 'Questa è la password'.encode('utf-8')
    __clearFile = ''
    __secureFile = 'gitpython/encrypted'

    def __init__(self, password='None', clear_file=None, secure_file=None):
        '''
        if password:
            self.__password = str(password).encode('utf-8')
        else:
            raise Exception('Password is needed')
            '''
        if clear_file:
            self.__clearFile = clear_file
        if secure_file:
            self.__secureFile = secure_file

    def _make_password(self, salt=None, password=None):
        if not salt:
            salt = os.urandom(128)
        if not password:
            password = self.__password
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        return base64.urlsafe_b64encode(kdf.derive(password)), salt

    def encrypt(self, message, on_file=False):
        salt = os.urandom(16)
        cipher_suite = Fernet(self._make_password(salt)[0])  # Key is generated and directly used
        cipher_text = cipher_suite.encrypt(message.encode('utf-8'))
        cipher_text_utf8 = base64.b64encode(salt).decode('utf-8') + cipher_text.decode('utf-8')
        # Scriviamo quindi il valore cifrato su un nuovo file:
        if on_file:
            with open(self.__secureFile, 'w') as encrypted_file:
                encrypted_file.write(cipher_text_utf8)
            return
        return cipher_text_utf8

    def file_encrypt(self, on_file=False):
        # Cifratura # Il messaggio da cifrare è all'interno di un file:
        with open(self.__clearFile, 'r') as file_to_encrypt:
            message = file_to_encrypt.read()
        salt = os.urandom(16)
        cipher_suite = Fernet(self._make_password(salt)[0])  # Key is generated and directly used
        cipher_text = cipher_suite.encrypt(message.encode('utf-8'))
        cipher_text_utf8 = base64.b64encode(salt).decode('utf-8') + cipher_text.decode('utf-8')
        # Scriviamo quindi il valore cifrato su un nuovo file:
        if on_file:
            with open(self.__secureFile, 'w') as encrypted_file:
                encrypted_file.write(cipher_text_utf8)
            return
        return cipher_text_utf8

    def decrypt(self, message, on_file=False):
        salt = base64.b64decode(message[:24].encode('utf-8'))
        cipher_suite = Fernet(self._make_password(salt)[0])
        plain_text = cipher_suite.decrypt(message[24:].encode('utf-8'))
        plain_text_utf8 = plain_text.decode('utf-8')
        # Scriviamo quindi il testo decifrato sul file decrypted.txt:
        if on_file:
            with open(self.__clearFile, 'w') as encrypted_file:
                encrypted_file.write(plain_text_utf8)
            return
        return plain_text_utf8

    def file_decrypt(self, on_file=False):
        # Decifratura # Decifriamo ora il file encrypted.txt:
        with open(self.__secureFile, 'r') as file_to_decrypt:
            message = file_to_decrypt.read()
        salt = base64.b64decode(message[:24].encode('utf-8'))
        cipher_suite = Fernet(self._make_password(salt)[0])
        plain_text = cipher_suite.decrypt(message[24:].encode('utf-8'))
        plain_text_utf8 = plain_text.decode('utf-8')
        # Scriviamo quindi il testo decifrato sul file decrypted.txt:
        if on_file:
            with open(self.__clearFile, 'w') as encrypted_file:
                encrypted_file.write(plain_text_utf8)
            return
        return plain_text_utf8
