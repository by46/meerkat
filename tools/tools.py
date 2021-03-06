import httplib
import logging
import os.path
import sys

import requests

if __name__ == '__main__':
    usage = "usage: python tools.py package_dir"
    if len(sys.argv) <= 1:
        print usage
        sys.exit(1)

    path = sys.argv[1]
    path = 'tools\\tmp'
    pkg = sorted([os.path.join(path, x) for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    # pkg = [r'D:\Git\meerkat\tools\\tmp\\lazy-object-proxy-1.2.2.tar.gz']
    url = 'http://scmesos06/'
    # url = 'http://localhost:8080/'
    with open('meerkat.log', 'wb') as w:
        for p in pkg:
            logging.error('process pkg: %s', p)
            files = {'content': (os.path.basename(p), open(p, 'rb'))}
            response = requests.post(url, files=files, data={':action': 'file_upload'})
            if response.status_code == httplib.OK:
                w.write('success %s' % os.path.basename(p))
            else:
                w.write('success code %s %s' % (response.status_code, os.path.basename(p)))
