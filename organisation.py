import json

def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)

def add_employee(username, employee_name):
    data = load_data()
    user = data.get(username)
    if user:
        user['employees'].append(employee_name)
        save_data(data)

def list_employees(username):
    data = load_data()
    user = data.get(username, {})
    return user.get('employees', [])

def add_department(username, department_name):
    data = load_data()
    user = data.get(username)
    if user:
        user['departments'].append(department_name)
        save_data(data)

def list_departments(username):
    data = load_data()
    user = data.get(username, {})
    return user.get('departments', [])
