from flask import Flask, request, redirect, send_file

app = Flask(__name__)

# Serve index.html (GET for normal, POST for login handling)
@app.route('/')
@app.route('/index.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'testuser' and password == 'Test@123':
            return redirect('/success.html')
        return send_file('index.html')  # Invalid login
    return send_file('index.html')  # Normal GET

# Serve success.html when login is successful
@app.route('/success.html')
def serve_success():
    return send_file('success.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
