import os.path

import requests

path = r'D:\Git\negowl\dist\negowl-0.0.9.zip'
files = {'content': (os.path.basename(path), open(path, 'rb'))}
url = 'http://localhost:8889/'
response = requests.post(url, files=files, data={':action': 'file_upload'})
print response.status_code
