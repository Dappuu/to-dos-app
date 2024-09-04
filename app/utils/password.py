import random
import string

from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)

def generate_password():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(16))
 