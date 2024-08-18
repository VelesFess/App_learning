import bcrypt


class PasswordEncryptor:
    @classmethod
    def encrypt(cls, password: str):
        return bcrypt.hashpw(password, bcrypt.gensalt())
    
    @classmethod
    def check(cls, plain_password: str, hashed_password: str):
        return bcrypt.checkpw(plain_password, hashed_password)
