import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC5b5cc34aa79e923ef19300f529218e07' 
    TWILIO_SYNC_SERVICE_SID = 'ISaa138820f694c2cce00ff58933a34eea' 
    TWILIO_API_KEY = 'SKef8645635da54bcf43ddcf9b34f07edf' 
    TWILIO_API_SECRET = 'kpRjWOE6DYgEokcLfMBxNuIrbgmO3V8b'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    txt = request.form['text']
    with open('newfile.txt', 'w') as f:
        f.write(txt)
    pathstore = 'newfile.txt'

    return send_file(pathstore, as_attachment=True)
    
    
        

    

    


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
