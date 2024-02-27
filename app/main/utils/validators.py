import re

def isEmailValid(email: str) -> bool:
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))