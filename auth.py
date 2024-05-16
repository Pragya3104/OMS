import json
import bcrypt

def load_users():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('data.json', 'w') as file:
        json.dump(users, file, indent=2)

def register_user(username, password, email):
    users = load_users()

    if username in users:
        return False

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = {'password': hashed_password.decode('utf-8'), 'email': email, 'employees': [], 'departments': []}
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()

    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]['password'].encode('utf-8')):
        return True
    return False

def logout_user():
    pass
