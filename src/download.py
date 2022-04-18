import gdown

url = 'https://drive.google.com/uc?id=1--FYOH2jT5Y7MoxzeESk_OjarTkom36a'
output = 'resources/model.h5'
gdown.download(url, output, quiet=False)