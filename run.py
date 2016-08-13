from gevent.wsgi import WSGIServer

from meerkat import app

if __name__ == '__main__':
    app.logger.info('Meerkat listening %s:%s', app.config['HTTP_HOST'], app.config['HTTP_PORT'])

    WSGIServer((app.config['HTTP_HOST'], app.config['HTTP_PORT']), application=app,
               log=app.config['WSGI_LOG']).serve_forever()
