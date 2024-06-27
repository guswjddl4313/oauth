from flask import Flask, redirect, request, session, render_template
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

OAUTH_PROVIDER_URL = os.getenv('OAUTH_PROVIDER_URL', 'http://3.34.84.134:20018')
CLIENT_ID = "Do-you-want-a-flag"
CLIENT_SECRET = "flag-is-here"
REDIRECT_URI = "http://3.34.84.134:20017/callback"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    state = os.urandom(8).hex()
    session['state'] = state
    oauth_url = f"{OAUTH_PROVIDER_URL}/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}"
    return redirect(oauth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    
    if state != session.pop('state', None):
        return "Invalid state parameter", 400

    token_response = requests.post(f"{OAUTH_PROVIDER_URL}/token", data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    user_info_response = requests.get(f"{OAUTH_PROVIDER_URL}/userinfo", headers={
        'Authorization': f"Bearer {token_response['access_token']}"
    }).json()

    return render_template('callback.html', user_info=user_info_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

