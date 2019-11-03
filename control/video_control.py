#!/usr/bin/python3

import json
import os
import sys

items_path = "/home/pi/repo/video_control/data/items.json"

def load_items(path):
    with open(path) as items_json:
        data = json.load(items_json)
        return data['items']

def apply_params(url, item, params):
    param_names = item.get('params', None)
    param_names_len = len(param_names) if param_names else 0

    if len(params) != param_names_len:
        sys.exit('wrong params count %d, expected %d params %s' % (len(params), param_names_len, str(param_names)))

    if params:
        url = url % dict(zip(param_names, (int(v) for v in params)))

    return url 

def run_video_dirrect_url(url):
    print("run omxplayer " + url)
    os.system('omxplayer ' + url)

def run_video_from_youtube(url):
    print("run youtube video " + url)
    os.system('omxplayer $(youtube-dl -g -f best %s)' % url)

def run_video(url):
    if(url.find("www.youtube.com") != -1):
        run_video_from_youtube(url)
    else:
        run_video_dirrect_url(url)    
    
def main():
    if len(sys.argv) < 2:
        sys.exit("name is empty")
    name = sys.argv[1]
    items = load_items(items_path)
    
    item = items.get(name, None)
    if not item:
        sys.exit('item "%s" not found' % name)

    url = item.get('url', None)
    if not url:
        sys.exit('item "%s": url not found: %s' % (name, str(item)))
    
    params = sys.argv[2:]
    url_with_params = apply_params(url, item, params)
    run_video(url_with_params)
  

if __name__ == '__main__':
    main()
