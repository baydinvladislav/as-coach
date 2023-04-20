import random
import string


def generate_random_password(length: int) -> str:
    """
    Generates a random password of a given length
    Args:
       length: length of result password
    """
    letters = string.ascii_letters + string.digits
    password = "".join(random.choice(letters) for _ in range(length))
    return password
