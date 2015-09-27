import os
import urllib2
import requests
import json
import data_helpers as dh
from flask import Flask, redirect, url_for, render_template, request
from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError
app = Flask(__name__)

client_id = "6c6cebd9c0b64628b6bbdb82b402577a"
app_uri = "http://mercer.herokuapp.com"

base_url = "https://instagram.com/oauth/authorize/?client_id="+ client_id + "&amp;redirect_uri=" + app_uri + "&amp;response_type=token"

instaConfig = {
  'client_id':os.environ.get('CLIENT_ID'),
  'client_secret':os.environ.get('CLIENT_SECRET'),
  'redirect_uri' : os.environ.get('REDIRECT_URI')
}
claraConfig = {
  'client_id':os.environ.get('CLARIFAI_APP_SECRET'),
  'client_secret':os.environ.get('CLARIFAI_APP_SECRET')
}

unauth_api = InstagramAPI(**instaConfig)

instagram_access_token = ""
code = None

@app.route('/callback')
def main():
  relevant_data = {}
  code = request.url.split("=")[1]
  access_token, user_info = unauth_api.exchange_code_for_access_token(code)
  instaConfig['access_token'] = access_token

  # api = InstagramAPI(**instaConfig)

  #media = api.user_liked_media(count=10)
  fun_url = "https://api.instagram.com/v1/users/self/media/liked?access_token=" + access_token + "&count=28"
  
  r = requests.get(fun_url)
  media = r.json()

  
  #media = unauth_api.media_popular(count=20)
  final_media = []
  result = []
  
  for m in media['data']:
    final_media.append(m['images']['low_resolution']["url"])

  relevant_data['final_media'] = final_media

  # instaConfig['tags'] = dh.get_clarifai(final_media)
  relevant_data['popular'] = dh.get_popular(access_token)

  #get clarafai on popular images
  relevant_data['clara_pop'] = dh.get_clarifai(relevant_data['popular'])
  print relevant_data['clara_pop']
  return render_template("index.html", relevant_data=relevant_data)
  # print "holla!!!!"
  # url = api.get_authorize_url(scope=["likes","comments"])
  # thing = requests.get(url)
  # print thing.json()
  # print result



@app.route('/')
def hello_world():
  auth_url = unauth_api.get_authorize_url(scope=["likes","comments"])
  return render_template("auth_page.html", auth_url=auth_url)
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
	app.run(host='0.0.0.0', port=port,debug=True)
