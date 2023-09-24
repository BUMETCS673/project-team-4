import bcrypt

def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password

def verify_password(password, hashed_password_from_db):
    password = password.encode('utf-8')  # Ensure password is bytes
    hashed_password_from_db = hashed_password_from_db.encode('utf-8')  # Ensure hashed_password_from_db is bytes
    return bcrypt.checkpw(password, hashed_password_from_db)




