from flask import Flask, render_template, request, redirect, url_for, session 
from auth import register_user , login_user, logout_user
from organisation import add_employee, list_employees, add_department, list_departments
from otp import send_otp, verify_otp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            session['temp_user'] = username
            send_otp(username)
            return redirect(url_for('otp'))
        else:
            return render_template('login.html', error="Invalid credentials. Try again.")
    return render_template('login.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        otp_code = request.form['otp']
        if verify_otp(session['temp_user'], otp_code):
            session['username'] = session.pop('temp_user')
            return redirect(url_for('dashboard'))
        else:
            return render_template('otp.html', error="Invalid OTP. Try again.")
    return render_template('otp.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if register_user(username, password, email):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Username already exists. Try again.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    employees = list_employees(session['username'])
    departments = list_departments(session['username'])
    return render_template('dashboard.html', employees=employees, departments=departments)

@app.route('/add_employee', methods=['POST'])
def add_employee_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    employee_name = request.form['employee_name']
    add_employee(session['username'], employee_name)
    return redirect(url_for('dashboard'))

@app.route('/add_department', methods=['POST'])
def add_department_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    department_name = request.form['department_name']
    add_department(session['username'], department_name)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
