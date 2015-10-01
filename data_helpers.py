import requests
from clarifai.client import ClarifaiApi


clarifai_api = ClarifaiApi()

def get_clarifai(list_of_media, *limit):
    media = list_of_media
    result = []
    dict_of_mediatags = []
    for m in media:
      image_tags = clarifai_api.tag_image_urls(m)
      result.append(image_tags)

    final_result = []
    for res in result:
      json_result = res["results"][0]["result"]["tag"]["classes"]

      for thing in json_result:
        thing = str(thing)
        final_result.append(str(thing))
      dict_of_mediatags.append({"url":res["results"][0]["url"],"tags": json_result})

    #print dict_of_mediatags[0]

    final_dict_list = {}

    for k in final_result:
      if k not in final_dict_list:
        final_dict_list[k] = final_result.count(k)

    tuple_arry = reversed(sorted(final_dict_list.items(), key=lambda x:x[1]))
    frequent_tags = []
   
    for tuple_obj in tuple_arry:
      frequent_tags.append({tuple_obj[0]:tuple_obj[1]})

    clarifai_result = {"frequent_tags":frequent_tags, "media_tags": dict_of_mediatags}

    return clarifai_result

def get_popular(access_token):
    base_url = "https://api.instagram.com/v1/media/popular?access_token=" + access_token
    r = requests.get(base_url)
    media = r.json()

    popular_images = []
    for m in media['data']:
      popular_images.append(m["images"]["low_resolution"]["url"])
    return popular_images