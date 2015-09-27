import os
import requests
from flask import Flask, redirect, url_for, render_template
from instagram.client import InstagramAPI
app = Flask(__name__)

client_id = "6c6cebd9c0b64628b6bbdb82b402577a"
app_uri = "http://mercer.herokuapp.com"

base_url = "https://instagram.com/oauth/authorize/?client_id="+ client_id + "&amp;redirect_uri=" + app_uri + "&amp;response_type=token"

instaConfig = {
  'client_id':os.environ.get('CLIENT_ID'),
  'client_secret':os.environ.get('CLIENT_SECRET'),
  'redirect_uri' : os.environ.get('REDIRECT_URI')
}
unauth_api = InstagramAPI(**instaConfig)

instagram_access_token = ""

@app.route('/callback')
@app.route('/callback/<code>')
def main():
  print "redirected"
  media = unauth_api.media_popular(count=20)
  final_media = []
  print "we are here"
  if code:
    print code
  for m in media:
    print m
    final_media.append(m.images['standard_resolution'].url)
    print m
  return render_template("index.html", final_media=final_media)
  # print "holla!!!!"
  # url = api.get_authorize_url(scope=["likes","comments"])
  # thing = requests.get(url)
  # print thing.json()

@app.route('/')
def hello_world():
  url = unauth_api.get_authorize_url(scope=["likes","comments"])
  return '<a href="%s">Connect with Instagram</a>' % url
  # if instagram info is in session variables, then display user photos
  # if 'instagram_access_token' in session and 'instagram_user' in session:
  #   userAPI = InstagramAPI(access_token=session['instagram_access_token'])
  #   recent_media, next = userAPI.user_recent_media(user_id=session['instagram_user'].get('id'),count=25)

  #   templateData = {
  #     'size' : request.args.get('size','thumb'),
  #     'media' : recent_media
  #   }
  #   print "TEST"



if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
