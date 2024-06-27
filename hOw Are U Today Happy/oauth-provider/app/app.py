from flask import Flask, request, jsonify, redirect
import os

app = Flask(__name__)

CLIENT_ID = "Do-you-want-a-flag"
CLIENT_SECRET = "flag-is-here"
REDIRECT_URI = "http://3.34.84.134:20017/callback"

db = {
    "auth_codes": {},
    "access_tokens": {}
}

@app.route('/authorize')
def authorize():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    state = request.args.get('state')

    if client_id != CLIENT_ID:
        return "Invalid client ID", 400

    auth_code = os.urandom(8).hex()
    db['auth_codes'][auth_code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri
    }
    
    return redirect(f"{redirect_uri}?code={auth_code}&state={state}")

@app.route('/token', methods=['POST'])
def token():
    code = request.form.get('code')
    redirect_uri = request.form.get('redirect_uri')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        return jsonify({"error": "invalid_client"}), 400

    if code not in db['auth_codes']:
        return jsonify({"error": "invalid_grant"}), 400

    if redirect_uri != db['auth_codes'][code]['redirect_uri']:
        return jsonify({"error": "invalid_grant"}), 400

    access_token = os.urandom(8).hex()
    db['access_tokens'][access_token] = {"username": "FLAG"}
    
    return jsonify({"access_token": access_token, "token_type": "bearer"})

@app.route('/userinfo')
def userinfo():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "missing_authorization_header"}), 400

    token = auth_header.split()[1]
    if token not in db['access_tokens']:
        return jsonify({"error": "invalid_token"}), 400

    return jsonify({
        "username": db['access_tokens'][token]['username'],
        "flag": "FLAG{04uth_i5_a_c0nv3nien7_me4n5_of_4uth3nticati0n!!}"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)

