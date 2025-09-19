


users = [
    {
        "username": "John",
        "password": "doe"
    }
]
def add_user(username: str, passwd: str) -> bool:
    user = [user for user in users if user['username'] == username]
    if len(user) == 0:
        users.append({
            "username": username,
            "password": passwd
        })
        return True
    return False

def check_user(username: str, password: str) -> bool:

    user = [user for user in users if user['username'] == username]
    if len(user) != 0:
        if user['password'] == password:
            return True
    return False