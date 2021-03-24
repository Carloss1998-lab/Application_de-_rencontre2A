import hashlib

class ChiffrerMotDePasse:

    def hash_password(password, idep):
        salt = idep
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest()
