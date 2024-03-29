"""Модуль для сущности шифратор."""

import base64
# pycryptodome
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


class Cipher:
    """Класс сущности - шифратор."""

    def __init__(self, password: str):
        self.__password = password

        # количество итераций (положительное целое число)
        # используемое в алгоритме PBKDF2 для усиления паролей
        self.__pbkdf2_iterations = 15000

        # желаемая длина ключа
        self.__dk_len = 32

    def set_password(self, password: str):
        """Сменить ключ для шифратора."""
        self.__password = password

    def base64_encoding(self, data_in: str) -> str:
        """Кодировать строку в формат Base64."""
        data_base64 = base64.b64encode(data_in)
        data_base64p = data_base64.decode("UTF-8")
        return data_base64p

    def base64_decoding(self, data_in: str) -> bytes:
        """Декодировать строку из формата Base64."""
        return base64.decodebytes(data_in.encode("UTF-8"))

    def generate_salt_32byte(self) -> bytes:
        """Генерировать 32-байтную случайную соль для хеширования паролей."""
        return get_random_bytes(32)

    def aes_cbc_pbkdf2_encrypt_to_base64(self, plaintext: str) -> str:
        """Зашифровать текст с помощью AES алгоритма."""
        password_bytes = self.__password.encode("UTF-8")
        salt = self.generate_salt_32byte()
        encryption_key = PBKDF2(
            password_bytes,
            salt,
            self.__dk_len,
            count=self.__pbkdf2_iterations,
            hmac_hash_module=SHA256
        )
        cipher = AES.new(encryption_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(
            pad(plaintext.encode("UTF-8"), AES.block_size))
        iv_base64 = self.base64_encoding(cipher.iv)
        salt_base64 = self.base64_encoding(salt)
        ciphertext_base64 = self.base64_encoding(ciphertext)
        return f"{salt_base64}:{iv_base64}:{ciphertext_base64}"

    def aes_cbc_pbkdf2_decrypt_from_base64(self, ciphertext_base64: str) -> str:
        """Расшифровать текст с помощью функции PBKDF2 в формате Base64."""
        password_bytes = self.__password.encode("UTF-8")
        data = ciphertext_base64.split(":")
        salt = self.base64_decoding(data[0])
        iv = self.base64_decoding(data[1])
        ciphertext = self.base64_decoding(data[2])
        decryption_key = PBKDF2(
            password_bytes,
            salt,
            self.__dk_len,
            count=self.__pbkdf2_iterations,
            hmac_hash_module=SHA256
        )
        cipher = AES.new(decryption_key, AES.MODE_CBC, iv)
        decryptedtext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        decryptedtext_p = decryptedtext.decode("UTF-8")
        return decryptedtext_p


# создаём шифратор с введёным ключём
# cipher = Cipher("0i&2M*2Hsq^rWLt1")

# текст для шифрования
# plaintext = "Проверка Check 1234!$^(*)ЫафQsf"
# print("plaintext: " + plaintext)

# print("\n* * * Encryption * * *")
# ciphertext_base64 = cipher.aes_cbc_pbkdf2_encrypt_to_base64(plaintext)
# print("ciphertext: " + ciphertext_base64)

# print("\n* * * Decryption * * *")
# decryptedtext = cipher.aes_cbc_pbkdf2_decrypt_from_base64(ciphertextBase64)
# print("plaintext: " + decryptedtext)
