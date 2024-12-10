from cryptography.fernet import Fernet
 
class PasswordEncrypter:     
 
    @classmethod
    def load_key(cls):
        """
        Load the encryption key.
        """
        if cls._key is None:
            raise ValueError("Encryption key is not set.")
        return cls._key
 
    @classmethod
    def encrypt_password(cls, password):
        """
        Encrypt the given password using the stored key.
 
        Args:
            password (str): The plaintext password to encrypt.
 
        Returns:
            str: The encrypted password (ciphertext).
        """
        key = "MTIzYmh1bmppa2lvPz8vMDAwMDAwMDAwMDAwMDAwMDA="
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_password.decode()
 
    @classmethod
    def decrypt_password(cls, encrypted_password):
        """
        Decrypt the given encrypted password using the stored key.
 
        Args:
            encrypted_password (str): The encrypted password (ciphertext).
 
        Returns:
            str: The decrypted plaintext password.
        """
        key = "MTIzYmh1bmppa2lvPz8vMDAwMDAwMDAwMDAwMDAwMDA="
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
 