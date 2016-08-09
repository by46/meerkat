import httplib
import logging

import requests
from flask import g

from meerkat import app

__author__ = 'benjamin.c.yan'


class Cabinet(object):
    def __init__(self, host, port=80):
        port = "" if port == 80 else (':' + str(port))
        self._session = requests.session()
        self.__upload_url = 'http://{host}{port}'.format(host=host, port=port)
        self.__download_url = 'http://{host}{port}'.format(host=host, port=port)

    def make_url(self, filename, special_path=None):
        group = app.config['DFIS_GROUP']
        file_type = app.config['DFIS_TYPE']
        if special_path:
            filename = special_path + "/" + filename
        return '{url}/{group}/{type}/{name}'.format(url=self.__download_url, group=group, type=file_type, name=filename)

    def upload(self, io, filename, user='cabinet-client', special_path=None):

        # if special_path:
        #     filename = special_path + "/" + filename
        group = app.config['DFIS_GROUP']
        file_type = app.config['DFIS_TYPE']
        method = 'UPDATE'
        logging.info("process {url}/{group}/{type}/{name}".format(url=self.__upload_url,
                                                                  group=group,
                                                                  type=file_type,
                                                                  name=filename))
        headers = {'FileGroup': group,
                   'FileType': file_type,
                   'FileMethod': method,
                   'FileName': filename,
                   'FileUser': user,
                   'SpecialFolderPath': special_path}
        response = self._session.post(self.__upload_url, headers=headers, data=io)
        if response.status_code == httplib.OK:
            logging.info("process success")
        else:
            logging.error("process error {code}".format(code=response.status_code))
        return response.status_code


def get_uploader():
    if not hasattr(g, '_cabinet'):
        g.dfis_cabinet = Cabinet(app.config['DFIS_HOST'], app.config['DFIS_PORT'])
    return g.dfis_cabinet


class Uploader(object):
    @staticmethod
    def upload(io, filename, user='cabinet-client', special_path=None):
        client = get_uploader()
        app.logger.info('upload package to dfis %s %s %s %s', app.config['DFIS_HOST'], app.config['DFIS_GROUP'],
                        app.config['DFIS_TYPE'],
                        filename)
        return client.upload(io, filename, user, special_path) == httplib.OK

    @staticmethod
    def make_url(filename):
        client = get_uploader()
        return client.make_url(filename)
