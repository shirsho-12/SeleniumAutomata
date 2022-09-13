import urllib.request
from urllib.request import urlretrieve
import requests

from bs4 import BeautifulSoup


for i in range(10):
    for j in range(10):
        for k in range(10):
            link = f"https://e-fop-site.netlify.app/3{i}{j}{k}"
