from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/role-select')
def role_select():
    return render_template('role-select.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
