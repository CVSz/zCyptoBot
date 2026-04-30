from cryptography.fernet import Fernet


class Envelope:
    """
    Envelope encryption; keys should be backed by KMS/HSM.
    """

    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, data: bytes) -> bytes:
        return self.cipher.encrypt(data)

    def decrypt(self, token: bytes) -> bytes:
        return self.cipher.decrypt(token)
