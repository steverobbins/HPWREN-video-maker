#!/usr/bin/env python3

import sys
import requests
import re

def main():
    args = sys.argv
    if len(args) < 2:
        exit('Source not specified', 1)
    response = requests.get(args[1])
    if response.status_code != 200:
        exit('Got bad response %d: %s' % (response.status_code, response.content.decode()), 2)
    qs = re.findall(r'href="(Q[0-9]+)/"', response.content.decode())
    for q in qs:
        response = requests.get('%s/%s' % (args[1], q))
        if response.status_code != 200:
            exit('Got bad response %d: %s' % (response.status_code, response.content.decode()), 3)
        files = re.findall(r'href="([0-9]+\.jpg)"', response.content.decode())
        for file in files:
            print('wget %s/%s/%s' % (args[1], q, file))

def exit(message, code=0):
    print(message)
    sys.exit(code)

if __name__ == '__main__':
    main()
