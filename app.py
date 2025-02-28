from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# Dummy user database (replace with a real database like SQLite for production)
users = {
    "test@example.com": {"password": "password123"}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return render_template('signin.html')
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash('Email already exists. Please use a different one.', 'danger')
            return render_template('signup.html')
        users[email] = {"password": password}
        flash('Sign-Up Successful. You can now sign in.', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/stock_tracker')
def stock_tracker():
    return render_template('stock_tracker.html')

@app.route('/live_stocks')
def live_stocks():
    return render_template('live_stocks.html')

@app.route('/stock_trends')
def stock_trends():
    return render_template('/stock_trends.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)