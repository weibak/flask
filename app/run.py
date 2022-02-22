import os
import redis

from flask import Flask, request, render_template, redirect, url_for, session, escape

app = Flask(__name__)
app.secret_key = "<Some secret key>"
app.config['SESSION_TYPE'] = 'filesystem'

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        value = None
        if "key" in request.values:
            value = request.values.get("key")
            redis_client.set("key", value)
    else:
        value = redis_client.get("key")
    return render_template("index.html", value=value)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect('get_email')
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # email = request.form.get('email')
        # password = request.form.get('password')
        # redis_client.set(email, password)
        # работает по разному, пытался разобраться в отличиях
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect(url_for('get_email'))
    return render_template('register.html')


@app.route('/get_email')
def get_email():
    if 'email' and 'password' in session:
        return 'Logged in as %s' % escape(session['email'])

    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('password', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
