import os
import requests
from flask import Flask, redirect
app = Flask(__name__)

client_id = "6c6cebd9c0b64628b6bbdb82b402577a"
app_uri = "http://mercer.heroku.com"

base_url = "https://instagram.com/oauth/authorize/?client_id="+ client_id + "&amp;redirect_uri=" + app_uri + "&amp;response_type=token"

@app.route('/')
def hello_world():
	access_code = requests.get(base_url)
	print access_code
	return '"Mercer" App! #fire'

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
