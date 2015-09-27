#THE MIT License (MIT)

# Copyright (c) 2015 Mustafa EL-Hilo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from instagram.client import InstagramAPI
from random import randint
import sys
from collections import OrderedDict

client_id = '6c6cebd9c0b64628b6bbdb82b402577a'
client_secret = 'bc0934df731244a497910f5d1f9b4bfa'
access_token = '16368135.6c6cebd.feba45715ee34a60b7570dec9dd49f26'
#client_ip = 'XX.XX.XX.XX'


api = InstagramAPI(client_id=client_id, client_secret=client_secret, client_ips= client_ip,access_token= access_token) 

media_all_ids=[]

#get recent media ids with the tag "instadogs", only get the most recent 80
#tag_recent_media returns 2 variables, the media ID in an array and the next 
#url for the next page
media_ids,next = api.tag_recent_media(tag_name='instadogs', count=80)

#obtain the max_tag_id to use to get the next page of results
temp,max_tag=next.split('max_tag_id=')
max_tag=str(max_tag)

for media_id in media_ids:
	media_all_ids.append(media_id.id)

counter = 1

#the while loop will go through the first 3 pages of resutls, you can increase this
# but you also need to increase the count above. 
while next and counter < 3 :
	more_media, next = api.tag_recent_media(tag_name='instadogs', max_tag_id=max_tag)
	temp,max_tag=next.split('max_tag_id=')
	max_tag=str(max_tag)
	for media_id2 in more_media:
		media_all_ids.append(media_id2.id)
	print len(media_all_ids)	
	counter+=1

#remove dublictes if any. 
media_all_ids=list(OrderedDict.fromkeys(media_all_ids))

print len(media_all_ids)
