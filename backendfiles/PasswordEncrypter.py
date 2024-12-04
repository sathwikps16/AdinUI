import bcrypt

class PasswordEncrypter:
    # Function to hash the password
    @staticmethod
    def hash_password(plain_password):
        # Generate a salt
        salt = bcrypt.gensalt()
        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_password