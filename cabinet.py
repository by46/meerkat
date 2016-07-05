import httplib
import logging
from cStringIO import StringIO

import requests

__author__ = 'benjamin.c.yan'


class Cabinet(object):
    def __init__(self, host, port=80):
        self.__upload_url = 'http://{host}:{port}'.format(host=host, port=port)
        self.__download_url = 'http://{host}:{port}'.format(host=host, port=port)

    def make_url(self, group, file_type, filename, special_path=None):
        if special_path:
            filename = special_path + "/" + filename
        return '{url}/{group}/{type}/{name}'.format(url=self.__download_url, group=group, type=file_type, name=filename)

    def upload(self, io, group, file_type, method, filename, user='cabinet-client', special_path=None):

        if special_path:
            filename = special_path + "/" + filename
        # filename = quote(filename)
        logging.info("process {url}/{group}/{type}/{name}".format(url=self.__upload_url,
                                                                  group=group,
                                                                  type=file_type,
                                                                  name=filename))
        headers = {'FileGroup': group,
                   'FileType': file_type,
                   'FileMethod': method,
                   'FileName': filename,
                   'FileUser': user,
                   'SpecialPath': special_path}
        response = requests.post(self.__upload_url, headers=headers, data=io)
        if response.status_code == httplib.OK:
            logging.info("process success")
        else:
            logging.error("process error {code}".format(code=response.status_code))
        return response.status_code

    def download(self, group, file_type, filename, special_path=None):
        if special_path:
            filename = special_path + "/" + filename
        url = '{url}/{group}/{type}/{name}'.format(url=self.__download_url, group=group, type=file_type, name=filename)
        logging.info('process {url}'.format(url=url))
        response = requests.get(url)
        if response.status_code == httplib.OK:
            logging.info("download success")
            return StringIO(response.content)
        else:
            logging.info("download failure, response code : {code}".format(code=response.status_code))
            return None
