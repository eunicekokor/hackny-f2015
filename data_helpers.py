import requests
from clarifai.client import ClarifaiApi


clarifai_api = ClarifaiApi()

def get_clarifai(list_of_media):
    media = list_of_media
    result = []
    for m in media:
      result.append(clarifai_api.tag_image_urls(m))

    final_result = []
    for res in result:
      json_result = res["results"][0]["result"]["tag"]["classes"]
      for thing in json_result:
        final_result.append(str(thing))

    final_dict_list = {}

    for k in final_result:
      if k not in final_dict_list:
        final_dict_list[k] = final_result.count(k)

    tuple_arry = reversed(sorted(final_dict_list.items(), key=lambda x:x[1]))
    frequent_tags = []
   
    for tuple_obj in tuple_arry:
      frequent_tags.append({tuple_obj[0]:tuple_obj[1]})

    return frequent_tags

def get_popular(access_token):
    base_url = "https://api.instagram.com/v1/media/popular?access_token=" + access_token
    r = requests.get(base_url)
    media = r.json()

    popular_images = []
    for m in media['data']:
      popular_images.append(m["images"]["low_resolution"]["url"])
    return popular_images