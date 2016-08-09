import httplib
import logging
import os
import os.path
import shutil

import requests

import pip

url = 'http://localhost:3141/'


def upload(package):
    logging.error('process pkg: %s', os.path.basename(package))
    files = {'content': (os.path.basename(package), open(package, 'rb'))}
    response = requests.post(url, files=files, data={':action': 'file_upload'})
    return response.status_code == httplib.OK


def main():
    tmp = 'tmp'
    if not os.path.exists(tmp):
        os.makedirs(tmp)

    req = 'requirements.txt'
    with open(req, 'rb') as r, open(req + '.back', 'wb') as w:
        for line in r:
            args = ['--proxy', 'http://localhost:3128', '-v', 'download', '-d', tmp, '-i',
                    'https://pypi.tuna.tsinghua.edu.cn/simple', line]
            pip.main(args)
            for package in os.listdir(tmp):
                package_full_path = os.path.join(tmp, package)
                if not upload(package_full_path):
                    logging.error('upload packages error %s', package)

            shutil.rmtree(tmp, ignore_errors=True)
            w.write(line)


if __name__ == '__main__':
    main()
