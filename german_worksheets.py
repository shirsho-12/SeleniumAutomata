import urllib3
from pathlib import Path
from tqdm import tqdm
import bs4
import wget

status_list = []
download_list = []
download_path = Path.home() / "Worksheets"
download_path.mkdir(parents=True, exist_ok=True)
print(download_path)

for i in tqdm(range(19, 25)):
    path = f"https://cls.nus.edu.sg/nusgerman/study-path.php?level=2&id={i}"
    # print(path)
    http = urllib3.PoolManager()
    r = http.request('GET', path)
    # print(r.status)
    status_list = status_list + [r.status]
    if r.status == 200:
        soup = bs4.BeautifulSoup(r.data, 'html.parser')
        for link in soup.find_all('a', href=True):
            if link['href'].endswith('.pdf'):
                print(link['href'])
                download_path = Path.home() / "Worksheets" / f"{i}"
                download_path.mkdir(parents=True, exist_ok=True)
                download_list = download_list + [link['href']]
                download_link = link['href']
                if (download_path / download_link.split('/')[-1]).exists():
                    print("File already exists")
                    continue
                try:
                    wget.download("https://cls.nus.edu.sg/nusgerman/" +
                                  download_link, str(download_path))
                except Exception:
                    print("Error")
                    print("https://cls.nus.edu.sg/nusgerman/" + download_link)
print(set(status_list))
print(len(download_list))
