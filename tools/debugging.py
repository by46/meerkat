import requests
import pip
if __name__ == '__main__':

    # x = requests.get('http://scmesos06/packages/recipe-0.0.1.zip#md5=ce82be85c817039fcd869e1a1c38f96c')
    session = requests.session()
    x = session.get('http://10.1.50.251/newegg/tool/pypi/recipe-0.0.1.zip')
    # x = session.get('http://neg-app-dfis-c4/newegg/tool/pypi/recipe-0.0.1.zip')
    assert x.status_code == 200
    with open('5.zip', 'wb') as w:
        w.write(x.content)
    # pip.main(['download', '--trusted-host', 'scmesos06', '-i', 'http://scmesos06/simple', 'recipe==0.0.1'])