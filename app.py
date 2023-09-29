from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password='1670',
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/')
def index():
    return redirect('/login')




@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            login = request.form.get('username')
            password = request.form.get('password')
            if (not login) or (not password):
                return render_template('invalidlogin.html')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
            records = list(cursor.fetchall())
            if not records:
                return render_template('invalidlogin.html')
            return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if (not name) or (not login) or (not password):
            return render_template('regfail.html')
        cursor.execute("SELECT login FROM service.users")
        checklog = cursor.fetchall()
        for row in checklog:
            if login == row[0]:
                return render_template('regfail2.html')
        if login == checklog[0]:
            return render_template('regfail.html',)
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);', (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')

