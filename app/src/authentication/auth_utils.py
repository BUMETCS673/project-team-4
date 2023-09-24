import bcrypt

def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password


def verify_password(password, hashed_password, salt):
    salted_password = (password + salt).encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(salted_password, hashed_password)



