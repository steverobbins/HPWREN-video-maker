#!/usr/bin/env python3

import json
import os
import re
import requests
import sys
import time

from dotenv import load_dotenv

load_dotenv()

def main():
    args = sys.argv
    if len(args) < 3:
        exit('Camera and date not specified', 1)

    camera = args[1]
    date = args[2]

    commands = open('download-images.sh', 'a')

    for i in range(1, 9):
        while True:
            response = apiRequest('post', params={
                'camera': camera,
                'date': date,
                'quaver': 'Q%s' % i,
            })
            print('api response for %s/%s/Q%s' % (camera, date, i))
            print(response.status_code)
            if response.status_code != 200:
                print(response.content.decode())
            if response.status_code >= 500:
                time.sleep(3)
            elif response.status_code != 200:
                exit('Got bad response %d: %s' % (response.status_code, response.content.decode()), 2)
            else:
                break
        data = json.loads(response.content.decode())
        if data and data.get('result'):
            for url in data['result']:
                parts = url.split('/')
                cacheFile = '../../../../cache/%s/%s/%s' % (date, parts[1], parts[-1])
                if os.path.isfile(cacheFile):
                    commands.write("cp %s ./\n" % cacheFile)
                else:
                    commands.write("wget %s/%s\n" % (
                        os.environ.get('HPWREN_IMAGE_URL', 'https://cdn.hpwren.ucsd.edu'),
                        url
                    ))

def apiRequest(method, url='', params={}):
        fullUrl = '%s%s' % (
            os.environ.get('HPWREN_API_URL', 'https://n87p8971w1.execute-api.us-west-2.amazonaws.com/prod'),
            '/' + url if url else ''
        )
        headers = {
            'x-api-key': os.environ.get('HPWREN_API_KEY'),
            'Origin': 'https://www.hpwren.ucsd.edu',
            'User-Agent': os.environ.get(
                'HPWREN_API_USER_AGENT',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            ),
        }
        if method == 'get':
            if len(params):
                url += '?'
                i = 0
                for key, value in params.items():
                    if i:
                        url += '&'
                    url += '%s=%s' % (key, value)
                    i += 1
            response = requests.get(fullUrl, headers=headers)
        elif method == 'post':
            headers['Content-Type'] = 'application/json'
            response = requests.post(fullUrl, headers=headers, data=json.dumps(params))
        return response

def exit(message, code=0):
    print(message)
    sys.exit(code)

if __name__ == '__main__':
    main()
