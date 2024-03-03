from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64


class Cipher:
    def __init__(self, password: str):
        self.__password = password

    def base64Encoding(self, input: str) -> str:
        dataBase64 = base64.b64encode(input)
        dataBase64P = dataBase64.decode("UTF-8")
        return dataBase64P

    def base64Decoding(self, input: str) -> bytes:
        return base64.decodebytes(input.encode("UTF-8"))

    def generateSalt32Byte(self) -> bytes:
        return get_random_bytes(32)

    def aesCbcPbkdf2EncryptToBase64(self, plaintext: str) -> str:
        passwordBytes = self.__password.encode("UTF-8")
        salt = self.generateSalt32Byte()
        PBKDF2_ITERATIONS = 15000
        encryptionKey = PBKDF2(
            passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256
        )
        cipher = AES.new(encryptionKey, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext.encode("UTF-8"), AES.block_size))
        ivBase64 = self.base64Encoding(cipher.iv)
        saltBase64 = self.base64Encoding(salt)
        ciphertextBase64 = self.base64Encoding(ciphertext)
        return saltBase64 + ":" + ivBase64 + ":" + ciphertextBase64

    def aesCbcPbkdf2DecryptFromBase64(self, ciphertextBase64: str) -> str:
        passwordBytes = self.__password.encode("UTF-8")
        data = ciphertextBase64.split(":")
        salt = self.base64Decoding(data[0])
        iv = self.base64Decoding(data[1])
        ciphertext = self.base64Decoding(data[2])
        PBKDF2_ITERATIONS = 15000
        decryptionKey = PBKDF2(
            passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256
        )
        cipher = AES.new(decryptionKey, AES.MODE_CBC, iv)
        decryptedtext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        decryptedtextP = decryptedtext.decode("UTF-8")
        return decryptedtextP


# создаём шифратор с введёным ключём
# cipher = Cipher("0i&2M*2Hsq^rWLt1")

# текст для шифрования
# plaintext = "Проверка Check 1234!$^(*)ЫафQsf"
# print("plaintext: " + plaintext)

# print("\n* * * Encryption * * *")
# ciphertextBase64 = cipher.aesCbcPbkdf2EncryptToBase64(plaintext)
# print("ciphertext: " + ciphertextBase64)

# print("\n* * * Decryption * * *")
# decryptedtext = cipher.aesCbcPbkdf2DecryptFromBase64(ciphertextBase64)
# print("plaintext: " + decryptedtext)
