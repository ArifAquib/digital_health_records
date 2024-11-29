import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role):
    with open("users.txt", "a") as file:
        hashed_password = hash_password(password)
        file.write(f"{username},{hashed_password},{role}\n")

def is_user_registered(username, password, role=None):
    hashed_password = hash_password(password)
    try:
        with open("users.txt", "r") as file:
            users = file.readlines()
        for user in users:
            user_data = user.strip().split(",")
            if user_data[0] == username and user_data[1] == hashed_password:
                if role is None or user_data[2] == role:
                    return True
    except FileNotFoundError:
        pass
    return False
