from flask import Flask, render_template, request, jsonify
import string
import secrets
import random

# Initialize Flask app
app = Flask(__name__)


def generate_password(length, use_lower, use_upper, use_digits, use_special):
    # Build pool
    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_special:
        pool += string.punctuation

    if not pool:
        return {"Error": "You must select at least one character set!"}

    # Ensure at least one char from each selected group for stronger password
    password_chars = []
    if use_lower:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        password_chars.append(secrets.choice(string.digits))
    if use_special:
        password_chars.append(secrets.choice(string.punctuation))

    # Fill the rest
    while len(password_chars) < length:
        password_chars.append(secrets.choice(pool))

    random.shuffle(password_chars)
    password = ''.join(password_chars)
    return {"password": password}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    # read inputs with defaults
    length = int(data.get('length', 12))
    use_lower = bool(data.get('lower', True))
    use_upper = bool(data.get('upper', True))
    use_digits = bool(data.get('digits', True))
    use_special = bool(data.get('special', False))

    result = generate_password(length, use_lower, use_upper, use_digits, use_special)
    return jsonify(result)

if __name__ == '__main__':
    # debug=True for development only
    app.run(host='0.0.0.0', port=5000, debug=True)
